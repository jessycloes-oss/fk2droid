package com.fk2droid;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.os.Bundle;
import android.os.Handler;
import android.preference.PreferenceManager;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.TextView;

import com.fk2droid.protocol.DongleSession;
import com.fk2droid.protocol.Msg;

/**
 * Ecran principal : affiche Android Auto en plein ecran et relaie le tactile et les touches.
 * La session avec le dongle vit dans {@link AutoService} : quitter cet ecran (reglages,
 * radio, navigation Honda...) ne coupe plus Android Auto.
 */
public class AutoActivity extends Activity implements SurfaceHolder.Callback, AutoService.Ui {

    private final Handler ui = new Handler();
    private SurfaceView surfaceView;
    private TextView status;
    /** Des images Android Auto arrivent : aucun message ne doit couvrir l'ecran. */
    private volatile boolean videoActive;
    /** Reglage de diagnostic : afficher le code des touches inconnues. */
    /** Message permanent a reafficher apres un message passager (null = ecran libre). */
    private String baseStatus;
    private AutoService service;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN
                | WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setContentView(R.layout.activity_auto);
        // Le fond noir de la mise en page suffit : pas de seconde couche a dessiner.
        getWindow().setBackgroundDrawable(null);

        surfaceView = (SurfaceView) findViewById(R.id.surface);
        status = (TextView) findViewById(R.id.status);
        surfaceView.getHolder().addCallback(this);
        surfaceView.setOnTouchListener(new View.OnTouchListener() {
            public boolean onTouch(View v, MotionEvent e) { return handleTouch(v, e); }
        });
        // Appui long sur le texte d'etat -> reglages
        status.setOnLongClickListener(new View.OnLongClickListener() {
            public boolean onLongClick(View v) {
                startActivity(new Intent(AutoActivity.this, SettingsActivity.class));
                return true;
            }
        });

        Intent svc = new Intent(this, AutoService.class);
        // Simulation sans dongle : uniquement dans un APK de test (debuggable), jamais en version normale.
        if ((getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE) != 0) {
            String simFile = getIntent().getStringExtra(AutoService.EXTRA_SIM_FILE);
            if (simFile != null) svc.putExtra(AutoService.EXTRA_SIM_FILE, simFile);
            // Test emulateur : decodeur OMX logiciel d'Android accepte a la place du materiel.
            if (getIntent().getBooleanExtra("omx_any", false)) com.fk2droid.video.OmxDecoder.allowSoftwareOmxForTests = true;
        }
        startService(svc);
    }

    @Override
    protected void onResume() {
        super.onResume();
        surfaceView.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LOW_PROFILE);
        startService(new Intent(this, AutoService.class));
        ui.post(attach);
    }

    /** Le service est cree par startService juste avant : on s'y accroche des qu'il existe. */
    private final Runnable attach = new Runnable() {
        public void run() {
            AutoService s = AutoService.get();
            if (s == null) { ui.postDelayed(this, 100); return; }
            service = s;
            videoActive = s.isVideoActive();
            baseStatus = videoActive ? null : s.baseStatus();
            if (baseStatus != null) {
                status.setText(baseStatus);
                status.setVisibility(View.VISIBLE);
            } else {
                status.setVisibility(View.INVISIBLE);
            }
            s.attachUi(AutoActivity.this);
            if (surface != null) s.setSurface(surface);
        }
    };

    @Override
    protected void onPause() {
        ui.removeCallbacks(attach);
        // On ne coupe plus la session : seul l'affichage s'arrete, Android Auto continue en arriere-plan.
        if (service != null) {
            service.detachUi(this);
            service.setSurface(null);
            service = null;
        }
        super.onPause();
    }

    // ---------------------------------------------------------------- Ecran / tactile

    private android.view.Surface surface;

    @Override
    public void surfaceCreated(SurfaceHolder h) { }

    @Override
    public void surfaceChanged(SurfaceHolder h, int format, int w, int hh) {
        surface = h.getSurface();
        if (service != null) service.setSurface(surface);
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder h) {
        surface = null;
        if (service != null) service.setSurface(null);
    }

    private boolean handleTouch(View v, MotionEvent e) {
        AutoService svc = service;
        DongleSession s = svc != null ? svc.session() : null;
        if (s == null) return false;
        AutoService sv = svc;
        if (sv != null && sv.config() != null && sv.config().multiTouch) {
            sendMultiTouch(s, v, e);
            return true;
        }
        int action;
        switch (e.getActionMasked()) {
            case MotionEvent.ACTION_DOWN: action = Msg.TOUCH_DOWN; break;
            case MotionEvent.ACTION_MOVE: action = Msg.TOUCH_MOVE; break;
            case MotionEvent.ACTION_UP:
            case MotionEvent.ACTION_CANCEL: action = Msg.TOUCH_UP; break;
            default: return true;
        }
        long t0 = System.nanoTime();
        s.sendTouch(action, e.getX() / v.getWidth(), e.getY() / v.getHeight());
        Stats.touchSent(System.nanoTime() - t0);
        return true;
    }

    private final float[] mtX = new float[10], mtY = new float[10];
    private final int[] mtA = new int[10], mtId = new int[10];

    /**
     * Tactile multipoint (pincer pour zoomer dans Maps) : tous les doigts a chaque evenement,
     * le doigt qui se pose ou se leve avec son action, les autres en glissement.
     */
    private void sendMultiTouch(DongleSession s, View v, MotionEvent e) {
        int masked = e.getActionMasked();
        int changed = e.getActionIndex();
        int n = Math.min(e.getPointerCount(), 10);
        float w = v.getWidth(), h = v.getHeight();
        for (int i = 0; i < n; i++) {
            mtX[i] = e.getX(i) / w;
            mtY[i] = e.getY(i) / h;
            mtId[i] = e.getPointerId(i);
            int a = Msg.MT_MOVE;
            if (i == changed) {
                if (masked == MotionEvent.ACTION_DOWN || masked == MotionEvent.ACTION_POINTER_DOWN) a = Msg.MT_DOWN;
                else if (masked == MotionEvent.ACTION_UP || masked == MotionEvent.ACTION_POINTER_UP) a = Msg.MT_UP;
            }
            if (masked == MotionEvent.ACTION_CANCEL) a = Msg.MT_UP;
            mtA[i] = a;
        }
        long t0 = System.nanoTime();
        s.sendMultiTouch(mtX, mtY, mtA, mtId, n);
        Stats.touchSent(System.nanoTime() - t0);
    }

    /** Touches multimedia (volant / facade) -> commandes Android Auto. */
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_MENU) {
            startActivity(new Intent(this, SettingsActivity.class));
            return true;
        }
        AutoService svc = AutoService.get();
        DongleSession s = svc != null ? svc.session() : null;
        boolean inCall = svc != null && svc.isInCall();
        // Honda Connect : la touche « raccrocher » du volant arrive comme RETOUR (code 4).
        // Pendant un appel, elle raccroche au lieu de quitter FK2Droid.
        if (keyCode == KeyEvent.KEYCODE_BACK && s != null && inCall) {
            s.sendCommand(Msg.CMD_REJECT_PHONE);
            return true;
        }
        // Volume au volant (codes Honda) : un cran par appui, repetition permise si maintenu.
        if (MediaKeys.isHondaVolume(keyCode)) {
            AutoService cs = AutoService.get();
            HondaSteering st = cs != null ? cs.steering() : null;
            // Touche que l'on vient de rendre au Honda : traitement normal du systeme.
            if (st != null && st.volumeToSystem()) return super.onKeyDown(keyCode, event);
            if (event.getRepeatCount() == 0) MediaKeys.volume(this, keyCode);
            return true;
        }
        // Une seule commande par appui (la repetition d'une touche maintenue est ignoree).
        if (MediaKeys.commandFor(keyCode, inCall) != 0) {
            if (event.getRepeatCount() == 0) MediaKeys.handle(this, keyCode, "ecran");
            return true;
        }
        if (event.getRepeatCount() == 0) MediaKeys.handle(this, keyCode, "ecran");
        return super.onKeyDown(keyCode, event);
    }

    // ---------------------------------------------------------------- Messages du service

    @Override
    public void onServiceStatus(String s, boolean permanent, boolean force) {
        if (permanent) setStatus(s);
        else showInfo(s, force);
    }

    @Override
    public void onVideoStarted() {
        // Premiere image Android Auto : on libere l'ecran de tout message.
        videoActive = true;
        ui.post(new Runnable() {
            public void run() {
                baseStatus = null;
                ui.removeCallbacks(restoreStatus);
                status.setVisibility(View.INVISIBLE);
            }
        });
    }

    // ---------------------------------------------------------------- Utilitaires

    /** Message permanent (attente, erreur, diagnostic) : reste affiche jusqu'au suivant. */
    private void setStatus(final String s) {
        ui.post(new Runnable() {
            public void run() {
                videoActive = false;
                baseStatus = s;
                ui.removeCallbacks(restoreStatus);
                status.setText(s);
                status.setVisibility(View.VISIBLE);
            }
        });
    }

    /**
     * Message passager : affiche 3 s puis retour au message permanent (ou rien).
     * Ignore pendant que Android Auto s'affiche, sauf si force (ex. « Android Auto connecte »).
     */
    private void showInfo(final String s, final boolean force) {
        ui.post(new Runnable() {
            public void run() {
                if (videoActive && !force) return;
                status.setText(s);
                status.setVisibility(View.VISIBLE);
                ui.removeCallbacks(restoreStatus);
                ui.postDelayed(restoreStatus, 3000);
            }
        });
    }

    private final Runnable restoreStatus = new Runnable() {
        public void run() {
            if (baseStatus != null && !videoActive) {
                status.setText(baseStatus);
                status.setVisibility(View.VISIBLE);
            } else {
                status.setVisibility(View.INVISIBLE);
            }
        }
    };
}
