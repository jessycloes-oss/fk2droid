package com.fk2droid;

import android.content.Context;
import android.os.Handler;
import android.util.Log;

import java.lang.reflect.Field;
import java.lang.reflect.Method;

/**
 * Etat du Honda Connect lu dans son service « StateMgrService » (Fujitsu Ten) :
 * - jour / nuit (suit l'eclairage du tableau de bord, donc les phares) -> mode nuit Android Auto ;
 * - adresse video (92 = camera de recul) -> retour sur Android Auto apres la marche arriere.
 *
 * Methode decouverte par MaKi83 (OpenDroidAuto). Implementation propre a FK2Droid : lecture par
 * reflexion toutes les 1,5 s, sans bibliotheque Honda dans l'APK. Sur un appareil qui n'est pas
 * un Honda Connect, le service est absent et cette classe ne fait rien.
 */
public class HondaState {
    private static final String TAG = "FK2Droid";
    private static final String SERVICE = "StateMgrService";
    private static final int STATE_NIGHT = 1;
    /** Adresse video de la camera de recul (OpenDroidAuto). */
    public static final int VIDEO_REAR_CAMERA = 92;
    private static final long POLL_MS = 1500;

    public interface Listener {
        void onNightChanged(boolean night);
        void onRearCamera(boolean active);
    }

    private final Context ctx;
    private final Handler handler = new Handler();
    private final Listener listener;
    private Object manager;
    private Method getAllState;
    private Field dayNight, videoAddress;
    private boolean started;
    private int lastDayNight = -1;
    private int lastVideo = -1;
    private volatile String diag = "pas encore lu";

    public HondaState(Context ctx, Listener l) {
        this.ctx = ctx;
        this.listener = l;
    }

    public void start() {
        if (started) return;
        started = true;
        try {
            manager = ctx.getSystemService(SERVICE);
            if (manager == null) {
                diag = "service absent (pas un Honda Connect ?)";
                return;
            }
            getAllState = manager.getClass().getMethod("getAllState");
        } catch (Throwable t) {
            manager = null;
            diag = "indisponible : " + t;
            return;
        }
        handler.post(poll);
    }

    public void stop() {
        started = false;
        handler.removeCallbacks(poll);
    }

    /** -1 inconnu, 0 jour, 1 nuit. */
    public int dayNight() { return lastDayNight; }

    public String diagnostic() {
        return diag;
    }

    private final Runnable poll = new Runnable() {
        public void run() {
            if (!started) return;
            read();
            handler.postDelayed(this, POLL_MS);
        }
    };

    private void read() {
        try {
            Object info = getAllState.invoke(manager);
            if (info == null) { diag = "aucun etat"; return; }
            if (dayNight == null) {
                dayNight = info.getClass().getField("dayNightState");
                videoAddress = info.getClass().getField("videoAddress");
            }
            int dn = dayNight.getInt(info) == STATE_NIGHT ? 1 : 0;
            int va = videoAddress.getInt(info);
            diag = (dn == 1 ? "nuit" : "jour") + ", ecran Honda " + va
                    + (va == VIDEO_REAR_CAMERA ? " (camera de recul)" : "");
            if (dn != lastDayNight) {
                boolean first = lastDayNight < 0;
                lastDayNight = dn;
                Log.i(TAG, "Honda : " + (dn == 1 ? "nuit" : "jour") + (first ? " (etat initial)" : ""));
                listener.onNightChanged(dn == 1);
            }
            if (va != lastVideo) {
                boolean wasCam = lastVideo == VIDEO_REAR_CAMERA;
                boolean isCam = va == VIDEO_REAR_CAMERA;
                lastVideo = va;
                if (isCam != wasCam) {
                    Log.i(TAG, "Honda : camera de recul " + (isCam ? "affichee" : "terminee"));
                    listener.onRearCamera(isCam);
                }
            }
        } catch (Throwable t) {
            diag = "erreur de lecture : " + t;
        }
    }
}
