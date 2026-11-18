package com.fk2droid.protocol;

/** Evenements remontes par la session (appeles depuis le thread de lecture USB). */
public interface DongleListener {
    /** phoneType : Msg.PHONE_* (5 = Android Auto, 3 = CarPlay, 1 = recopie Android, 4 = recopie iPhone). */
    void onPhoneConnected(int phoneType, boolean wireless);

    void onPhoneDisconnected();

    /** Trame H.264 Annex-B (data[off..off+len]). */
    void onVideo(int width, int height, byte[] data, int off, int len);

    /** PCM 16 bits little-endian. */
    void onAudio(int decodeType, byte[] data, int off, int len);

    /** Commande audio (debut/fin media, appel, Siri, navigation...). */
    void onAudioCommand(int command);

    void onStatus(String message);

    void onError(Exception e);
}
