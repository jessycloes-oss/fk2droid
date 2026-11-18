package com.fk2droid.protocol;

/** Reglages de session. Valeurs par defaut adaptees a l'ecran 7" (800x480) du Honda Connect. */
public class DongleConfig {
    public int width = 800;
    public int height = 480;
    /** 30 i/s : le decodage logiciel du Tegra sous Android 4.0.4 ne suivra pas 60 i/s. */
    public int fps = 30;
    public int dpi = 160;
    public boolean nightMode = false;
    /** 0 = conduite a gauche (Europe continentale), 1 = conduite a droite (UK). */
    public int handDrive = 0;
    public String boxName = "FK2Droid";
    public boolean wifi5g = true;
    /** true = micro de l'autoradio (AudioRecord) ; false = micro integre au dongle s'il en a un. */
    public boolean useCarMic = true;
    /** true = audio Android Auto renvoye par USB et joue par l'application. */
    public boolean audioOverUsb = true;
    /**
     * Appels via le kit mains libres d'origine (HandsFreeLink) : musique par USB, et au debut
     * d'un appel le dongle bascule le son en Bluetooth pour que la voiture prenne l'appel avec
     * son propre micro. Utile quand le micro de la voiture est inaccessible aux applis (Honda Connect).
     */
    public boolean callsViaCarBluetooth = false;
    /** Fin d'appel : revenir tout de suite a l'ecran Android Auto s'il etait affiche avant l'appel. */
    public boolean returnAfterCall = true;
    /** Decodage allege automatique quand l'autoradio n'arrive plus a suivre. */
    public boolean adaptiveVideo = true;
    public int mediaDelayMs = 300;
    /**
     * Mode Android Auto du dongle (fichier /etc/android_work_mode = 1). Indispensable : sans lui,
     * le CPC200-CCPA ne propose que CarPlay au telephone Android.
     */
    public boolean androidWorkMode = true;
    /** Tactile multipoint (message 0x17) : pincer pour zoomer dans Google Maps. */
    public boolean multiTouch = false;
}
