package com.fk2droid;

import android.app.Notification;
import android.app.PendingIntent;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbManager;
import android.os.Handler;
import android.os.IBinder;
import android.preference.PreferenceManager;
import android.view.Surface;

import com.fk2droid.audio.AudioOutput;
import com.fk2droid.audio.MicInput;
import com.fk2droid.protocol.DongleConfig;
import com.fk2droid.protocol.DongleListener;
import com.fk2droid.protocol.DongleSession;
import com.fk2droid.protocol.Msg;
import com.fk2droid.protocol.Transport;
import com.fk2droid.sim.SimTransport;
import com.fk2droid.usb.UsbTransport;
import com.fk2droid.video.VideoPipeline;

/**
 * Garde la session avec le dongle ouverte en arriere-plan (service au premier plan).
 *
 * Avant la 1.5, quitter l'ecran Android Auto fermait la session : le dongle, prive de battement
 * de coeur, redemarrait apres ~15-20 s et son rebranchement USB relancait FK2Droid par-dessus
 * l'appli ouverte. Ici la session vit tant que le dongle est branche : musique, appels et
 * battement de coeur continuent pendant que l'on navigue dans le Honda Connect.
 */
public class AutoService extends Service implements DongleListener,
        VideoPipeline.KeyframeRequester, VideoPipeline.StatusSink, HondaState.Listener {

    /** Ecran Android Auto (null quand il n'est pas affiche). */
    public interface Ui {
        void onServiceStatus(String message, boolean permanent, boolean force);
        void onVideoStarted();
    }

    static final String EXTRA_SIM_FILE = "sim_file";
    private static final String ACTION_USB_PERMISSION = "com.fk2droid.USB_PERMISSION";
    private static final long RETRY_MS = 3000;
    private static final int NOTIF_ID = 1;

    private static volatile AutoService instance;

    public static AutoService get() { return instance; }

    private final Handler handler = new Handler();
    private UsbManager usb;
    private VideoPipeline video;
    private AudioOutput audio;
    private HondaSteering steering;
    private HondaState honda;
    /** Android Auto etait affiche quand la camera de recul est apparue : on y revient apres. */
    private volatile boolean returnAfterCamera;
    /** Type du telephone connecte (Msg.PHONE_*), 0 si aucun. */
    private volatile int phoneType;
    /** Relances de session faute d'image cle (limitees pour ne pas boucler). */
    private int keyframeRestarts;
    private static final int MAX_KEYFRAME_RESTARTS = 2;
    /** Retour apres la camera : le Honda reaffiche d'abord son ecran, on passe devant. */
    private static final long AFTER_CAMERA_MS = 700;
    private volatile DongleSession session;
    private volatile MicInput mic;
    private volatile DongleConfig config;
    private volatile Ui ui;
    private volatile boolean videoActive;
    private volatile boolean inCall;
    private volatile boolean callOnCarBluetooth;
    /** L'ecran Android Auto etait affiche (ou l'etait il y a peu) au debut de l'appel : on y revient a la fin. */
    private volatile boolean returnAfterCall;
    /** Dernier moment ou l'ecran Android Auto etait affiche (uptime ms). */
    private volatile long lastUiShown;
    /** Le Honda peut afficher son ecran telephone juste avant que l'appel ne nous soit signale. */
    private static final long RECENT_UI_MS = 60000;
    /** Seconde tentative si le Honda reprend la main juste apres notre retour. */
    private static final long BRING_BACK_RETRY_MS = 1500;
    /** Decodage en arriere-plan conserve quelques secondes apres l'appel, le temps du retour. */
    private static final long BACKGROUND_DECODE_GRACE_MS = 4000;
    private volatile String baseStatus = "Connexion au dongle...";
    private boolean permissionPending;
    private boolean connecting;
    private DongleSession lastSession;
    private String simFile;

    @Override
    public void onCreate() {
        super.onCreate();
        instance = this;
        usb = (UsbManager) getSystemService(Context.USB_SERVICE);
        video = new VideoPipeline(this, this);
        audio = new AudioOutput();
        config = loadConfig(this);
        video.setAdaptive(config.adaptiveVideo);
        steering = new HondaSteering(this);
        steering.bind();
        // Jour / nuit et camera de recul du Honda Connect
        honda = new HondaState(this, this);
        honda.start();

        IntentFilter f = new IntentFilter(ACTION_USB_PERMISSION);
        f.addAction(UsbManager.ACTION_USB_DEVICE_DETACHED);
        registerReceiver(usbReceiver, f);
        goForeground();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent != null && intent.getStringExtra(EXTRA_SIM_FILE) != null) {
            simFile = intent.getStringExtra(EXTRA_SIM_FILE);
        }
        connect();
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        instance = null;
        MediaKeys.release(this);
        steering.unbind();
        honda.stop();
        unregisterReceiver(usbReceiver);
        disconnect();
        video.release();
        audio.release();
        stopForeground(true);
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent i) { return null; }

    /** Service au premier plan : Android (et le Honda Connect) ne le tue pas en arriere-plan. */
    @SuppressWarnings("deprecation")
    private void goForeground() {
        Intent open = new Intent(this, AutoActivity.class)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        PendingIntent pi = PendingIntent.getActivity(this, 0, open, 0);
        Notification n = new Notification.Builder(this)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("FK2Droid")
                .setContentText("Android Auto actif - toucher pour revenir")
                .setContentIntent(pi)
                .setOngoing(true)
                .getNotification();
        startForeground(NOTIF_ID, n);
    }

    // ---------------------------------------------------------------- Ecran Android Auto

    public void attachUi(Ui u) {
        ui = u;
        applyConfig(loadConfig(this));
        MediaKeys.claim(this);
        // Touches piste suivante / precedente du volant : service propre au Honda Connect.
        steering.setActive(true);
        connect();
    }

    public void detachUi(Ui u) {
        if (ui == u) {
            ui = null;
            steering.setActive(false);
            lastUiShown = android.os.SystemClock.uptimeMillis();
        }
    }

    public void setSurface(Surface s) { video.setSurface(s); }

    public DongleSession session() { return session; }
    public HondaSteering steering() { return steering; }
    public boolean isVideoActive() { return videoActive; }
    public boolean isInCall() { return inCall; }
    public int phoneType() { return phoneType; }
    public HondaState honda() { return honda; }
    public DongleConfig config() { return config; }
    public String baseStatus() { return baseStatus; }

    /**
     * Nouveaux reglages : ceux envoyes au dongle a l'ouverture imposent de rouvrir la session,
     * les autres (appels via la voiture...) s'appliquent tout de suite.
     */
    private synchronized void applyConfig(DongleConfig c) {
        DongleConfig old = config;
        resolveNight(c);
        if (old != null && session != null && old.nightMode != c.nightMode) sendNight(c.nightMode);
        config = c;
        video.setAdaptive(c.adaptiveVideo);
        if (session != null && !initKey(old).equals(initKey(c))) {
            android.util.Log.i("FK2Droid", "Reglages modifies : reouverture de la session");
            disconnect();
            handler.postDelayed(retry, 500);
        }
    }

    private static String initKey(DongleConfig c) {
        // Le mode nuit n'en fait pas partie : il change en direct (commandes 16 / 17).
        return c.width + "x" + c.height + "@" + c.fps + "/" + c.dpi + "/" + c.boxName + "/" + c.handDrive
                + "/" + c.wifi5g + "/" + c.useCarMic + "/" + c.audioOverUsb;
    }

    // ---------------------------------------------------------------- Connexion USB

    private void connect() {
        synchronized (this) {
            if (session != null || connecting) return;
        }
        handler.removeCallbacks(retry);
        if (simFile != null) {
            startOpen(null);
            return;
        }
        UsbDevice dongle = findDongle();
        if (dongle == null) {
            status("Branchez le dongle Carlinkit sur le port USB...\n" + usbDiagnostic(), true, false);
            handler.postDelayed(retry, RETRY_MS);
            return;
        }
        if (!usb.hasPermission(dongle)) {
            if (!permissionPending) {
                permissionPending = true;
                status("Autorisez l'acces au dongle USB", true, false);
                PendingIntent pi = PendingIntent.getBroadcast(this, 0, new Intent(ACTION_USB_PERMISSION), 0);
                usb.requestPermission(dongle, pi);
            }
            return;
        }
        startOpen(dongle);
    }

    private void startOpen(final UsbDevice dev) {
        synchronized (this) { connecting = true; }
        new Thread(new Runnable() {
            public void run() { openSession(dev); }
        }, "connect").start();
    }

    private void openSession(UsbDevice dev) {
        DongleSession prev;
        synchronized (this) { prev = lastSession; }
        // Le dongle ne doit jamais etre ouvert deux fois : on attend la fin de l'ancienne session.
        if (prev != null) prev.awaitTermination(4000);
        Transport t = null;
        boolean opened = false;
        try {
            t = dev == null ? new SimTransport(simFile) : new UsbTransport(usb, dev);
            resolveNight(config);
            DongleSession s = new DongleSession(t, config, this);
            synchronized (this) {
                if (instance != this) { t.close(); return; }
                session = s;
                lastSession = s;
                mic = new MicInput(this, s);
                opened = true;
            }
            s.start();
        } catch (Exception e) {
            if (t != null && !opened) t.close();
            onError(e);
        } finally {
            synchronized (this) { connecting = false; }
        }
    }

    private synchronized void disconnect() {
        handler.removeCallbacks(retry);
        videoActive = false;
        inCall = false;
        callOnCarBluetooth = false;
        returnAfterCall = false;
        video.setBackgroundDecode(false);
        video.reset();
        if (mic != null) { mic.stop(); mic = null; }
        if (session != null) { session.stop(); session = null; }
        audio.stopAll();
    }

    /**
     * Fin d'appel : sans attendre que le Honda Connect quitte son ecran telephone (plusieurs
     * secondes), on remet tout de suite l'ecran Android Auto au premier plan. L'image a ete tenue
     * a jour pendant l'appel : elle s'affiche instantanement.
     */
    private final Runnable claimMediaKeys = new Runnable() {
        public void run() { MediaKeys.claim(AutoService.this); }
    };

    private final Runnable bringBack = new Runnable() {
        public void run() {
            if (ui != null || session == null || inCall) return;
            android.util.Log.i("FK2Droid", "Fin d'appel : retour a l'ecran Android Auto");
            startActivity(new Intent(AutoService.this, AutoActivity.class)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_REORDER_TO_FRONT));
        }
    };

    private final Runnable stopBackgroundDecode = new Runnable() {
        public void run() {
            if (!inCall) video.setBackgroundDecode(false);
        }
    };

    private final Runnable retry = new Runnable() {
        public void run() { connect(); }
    };

    private UsbDevice findDongle() {
        for (UsbDevice d : usb.getDeviceList().values()) {
            if (UsbTransport.isDongle(d)) return d;
        }
        return null;
    }

    /** Ce que voit Android sur le bus USB : sert a diagnostiquer le Honda Connect. */
    private String usbDiagnostic() {
        try {
            boolean host = getPackageManager().hasSystemFeature(PackageManager.FEATURE_USB_HOST);
            StringBuilder sb = new StringBuilder("[USB hote Android : ").append(host ? "oui" : "NON");
            int n = 0;
            for (UsbDevice d : usb.getDeviceList().values()) {
                if (n++ < 4) sb.append(n == 1 ? " | vus : " : ", ")
                        .append(String.format("%04x:%04x", d.getVendorId(), d.getProductId()));
            }
            if (n == 0) sb.append(" | aucun peripherique vu");
            return sb.append("]").toString();
        } catch (Exception e) {
            return "[USB : " + e + "]";
        }
    }

    private final BroadcastReceiver usbReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context c, Intent i) {
            if (ACTION_USB_PERMISSION.equals(i.getAction())) {
                permissionPending = false;
                if (i.getBooleanExtra(UsbManager.EXTRA_PERMISSION_GRANTED, false)) connect();
                else status("Permission USB refusee", true, false);
            } else if (UsbManager.ACTION_USB_DEVICE_DETACHED.equals(i.getAction())) {
                UsbDevice d = (UsbDevice) i.getParcelableExtra(UsbManager.EXTRA_DEVICE);
                if (UsbTransport.isDongle(d)) {
                    disconnect();
                    if (ui == null) {
                        // Dongle retire pendant que FK2Droid est en arriere-plan : on s'arrete.
                        // Le rebranchement relancera FK2Droid automatiquement.
                        stopSelf();
                    } else {
                        status("Dongle debranche", true, false);
                        handler.postDelayed(retry, RETRY_MS);
                    }
                }
            }
        }
    };

    // ---------------------------------------------------------------- Evenements dongle

    @Override
    public void onPhoneConnected(int phoneType, boolean wireless) {
        this.phoneType = phoneType;
        String s;
        switch (phoneType) {
            case Msg.PHONE_ANDROID_AUTO: s = "Android Auto connecte"; break;
            case Msg.PHONE_CARPLAY: s = "CarPlay connecte (iPhone)"; break;
            case Msg.PHONE_ANDROID_MIRROR: s = "Recopie d'ecran Android connectee"; break;
            default: s = "Telephone connecte (type " + phoneType + ")"; break;
        }
        s += wireless ? " (sans fil)" : " (filaire)";
        Stats.phone(s);
        baseStatus = null;
        status(s, false, true);
    }

    @Override
    public void onPhoneDisconnected() {
        audio.stopAll();
        videoActive = false;
        phoneType = 0;
        Stats.phone("deconnecte");
        status("Telephone deconnecte - en attente...", true, false);
    }

    @Override
    public void onVideo(int w, int h, byte[] data, int off, int len) {
        if (!videoActive) {
            videoActive = true;
            keyframeRestarts = 0;
            baseStatus = null;
            Ui u = ui;
            if (u != null) u.onVideoStarted();
        }
        // Sans ecran (FK2Droid en arriere-plan), les images sont simplement ignorees.
        video.submit(w, h, data, off, len);
    }

    @Override
    public void onAudio(int decodeType, byte[] data, int off, int len) {
        audio.write(decodeType, data, off, len);
    }

    @Override
    public void onAudioCommand(int cmd) {
        MicInput m = mic;
        DongleConfig c = config;
        switch (cmd) {
            case Msg.AUDIO_PHONECALL_START:
                if (!inCall) {
                    returnAfterCall = ui != null
                            || android.os.SystemClock.uptimeMillis() - lastUiShown < RECENT_UI_MS;
                    handler.removeCallbacks(stopBackgroundDecode);
                    // L'image Android Auto reste a jour pendant l'appel (peu de calcul : ecran d'appel).
                    if (returnAfterCall && c.returnAfterCall) video.setBackgroundDecode(true);
                }
                inCall = true;
                if (c.callsViaCarBluetooth && c.audioOverUsb) {
                    // L'appel part sur le Bluetooth de la voiture (micro et touches d'origine).
                    DongleSession s = session;
                    if (s != null) s.sendCommand(Msg.CMD_AUDIO_TRANSFER_ON);
                    callOnCarBluetooth = true;
                } else if (c.useCarMic && m != null) {
                    m.start();
                }
                break;
            case Msg.AUDIO_PHONECALL_STOP:
                Stats.callEnded();
                inCall = false;
                if (m != null) m.stop();
                if (callOnCarBluetooth) {
                    callOnCarBluetooth = false;
                    DongleSession s = session;
                    if (s != null) s.sendCommand(Msg.CMD_AUDIO_TRANSFER_OFF);
                }
                if (returnAfterCall && c.returnAfterCall) {
                    handler.post(bringBack);
                    handler.postDelayed(bringBack, BRING_BACK_RETRY_MS);
                }
                returnAfterCall = false;
                handler.postDelayed(stopBackgroundDecode, BACKGROUND_DECODE_GRACE_MS);
                break;
            case Msg.AUDIO_MEDIA_START:
                // La radio Honda a pu reprendre la main : FK2Droid redevient le lecteur actif
                // pour recevoir piste suivante / precedente du volant.
                handler.post(claimMediaKeys);
                break;
            case Msg.AUDIO_SIRI_START:
                if (c.useCarMic && m != null) m.start();
                break;
            case Msg.AUDIO_SIRI_STOP:
                if (m != null) m.stop();
                break;
            default:
                break;
        }
    }

    @Override
    public void onStatus(String message) {
        android.util.Log.i("FK2Droid", message);
        if (message.startsWith("Dongle initialise")) {
            status(message, true, false);
            handler.post(claimMediaKeys);
        }
        else status(message, false, false);
    }

    @Override
    public void onError(Exception e) {
        android.util.Log.w("FK2Droid", "Erreur session", e);
        videoActive = false;
        inCall = false;
        status("Erreur : " + e.getMessage() + " - nouvelle tentative...", true, false);
        handler.post(new Runnable() {
            public void run() {
                disconnect();
                handler.postDelayed(retry, RETRY_MS);
            }
        });
    }

    @Override
    public void requestKeyframe() {
        DongleSession s = session;
        if (s != null) s.sendCommand(Msg.CMD_REQUEST_KEYFRAME);
    }

    /**
     * L'ecran est affiche mais le telephone ne renvoie pas d'image cle (Android Auto ne repond pas
     * toujours a la commande 12 a travers le dongle). Seule parade sure : rouvrir la session, le
     * telephone recommence alors la projection par une image complete.
     */
    @Override
    public void onKeyframeTimeout() {
        handler.post(new Runnable() {
            public void run() {
                if (ui == null || session == null || inCall) return;
                boolean auto = PreferenceManager.getDefaultSharedPreferences(AutoService.this)
                        .getBoolean("restart_on_black", true);
                if (!auto || keyframeRestarts >= MAX_KEYFRAME_RESTARTS) {
                    status("Pas d'image du telephone : debranchez / rebranchez le dongle", true, false);
                    return;
                }
                keyframeRestarts++;
                android.util.Log.w("FK2Droid", "Pas d'image cle : reouverture de la session (" + keyframeRestarts + ")");
                status("Image perdue : reconnexion d'Android Auto...", true, false);
                disconnect();
                handler.postDelayed(retry, 1000);
            }
        });
    }

    // ---------------------------------------------------------------- Etat du Honda

    /** Choisit le mode nuit selon le reglage : phares du Honda (defaut), toujours jour, toujours nuit. */
    private void resolveNight(DongleConfig c) {
        String src = PreferenceManager.getDefaultSharedPreferences(this).getString("night_source", "honda");
        if ("night".equals(src)) c.nightMode = true;
        else if ("day".equals(src)) c.nightMode = false;
        else c.nightMode = honda != null && honda.dayNight() == 1;
    }

    private void sendNight(boolean night) {
        DongleSession s = session;
        if (s == null) return;
        s.sendQuietly(com.fk2droid.protocol.Messages.sendNumber("/tmp/night_mode", night ? 1 : 0));
        s.sendCommand(night ? Msg.CMD_NIGHT_ON : Msg.CMD_NIGHT_OFF);
    }

    @Override
    public void onNightChanged(boolean night) {
        DongleConfig c = config;
        boolean before = c.nightMode;
        resolveNight(c);
        if (c.nightMode != before) {
            android.util.Log.i("FK2Droid", "Mode nuit Android Auto : " + c.nightMode);
            sendNight(c.nightMode);
        }
    }

    private final Runnable backFromCamera = new Runnable() {
        public void run() {
            if (ui != null || session == null || inCall) return;
            android.util.Log.i("FK2Droid", "Fin de la camera de recul : retour a Android Auto");
            startActivity(new Intent(AutoService.this, AutoActivity.class)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_REORDER_TO_FRONT));
        }
    };

    @Override
    public void onRearCamera(boolean active) {
        boolean wanted = PreferenceManager.getDefaultSharedPreferences(this).getBoolean("return_after_camera", true);
        if (active) {
            handler.removeCallbacks(backFromCamera);
            returnAfterCamera = wanted && session != null && (ui != null
                    || android.os.SystemClock.uptimeMillis() - lastUiShown < 5000);
        } else if (returnAfterCamera) {
            returnAfterCamera = false;
            handler.postDelayed(backFromCamera, AFTER_CAMERA_MS);
            handler.postDelayed(backFromCamera, AFTER_CAMERA_MS + BRING_BACK_RETRY_MS);
        }
    }

    @Override
    public void onDecoderStatus(String s) {
        android.util.Log.i("FK2Droid", s);
        if (s.startsWith("Aucun")) status(s, true, false);
    }

    private void status(String s, boolean permanent, boolean force) {
        if (permanent) baseStatus = s;
        Ui u = ui;
        if (u != null) u.onServiceStatus(s, permanent, force);
    }

    static DongleConfig loadConfig(Context ctx) {
        SharedPreferences p = PreferenceManager.getDefaultSharedPreferences(ctx);
        DongleConfig c = new DongleConfig();
        String res = p.getString("resolution", "800x480");
        String[] wh = res.split("x");
        try {
            c.width = Integer.parseInt(wh[0]);
            c.height = Integer.parseInt(wh[1]);
            c.fps = Integer.parseInt(p.getString("fps", "30"));
        } catch (Exception ignored) { }
        c.handDrive = p.getBoolean("right_hand_drive", false) ? 1 : 0;
        try {
            c.dpi = Integer.parseInt(p.getString("dpi", "160"));
        } catch (NumberFormatException ignored) { }
        c.multiTouch = p.getBoolean("multi_touch", false);
        c.boxName = p.getString("box_name", "FK2Droid").trim();
        if (c.boxName.length() == 0) c.boxName = "FK2Droid";
        if (c.boxName.length() > 16) c.boxName = c.boxName.substring(0, 16); // limite du dongle
        c.wifi5g = p.getBoolean("wifi_5g", true);
        c.useCarMic = p.getBoolean("car_mic", true);
        c.audioOverUsb = p.getBoolean("audio_usb", true);
        c.callsViaCarBluetooth = p.getBoolean("calls_car_bt", false);
        c.returnAfterCall = p.getBoolean("return_after_call", true);
        c.adaptiveVideo = p.getBoolean("adaptive_video", true);
        String dt = p.getString("display_thread", "auto");
        VideoPipeline.preferHardware = !"sw".equals(p.getString("video_decoder", "auto"));
        VideoPipeline.forceDisplayThread = "on".equals(dt) ? Boolean.TRUE : "off".equals(dt) ? Boolean.FALSE : null;
        try {
            com.fk2droid.video.FfmpegDecoder.forcedFormat = Integer.parseInt(p.getString("video_format", "0"));
        } catch (NumberFormatException ignored) { }
        return c;
    }
}
