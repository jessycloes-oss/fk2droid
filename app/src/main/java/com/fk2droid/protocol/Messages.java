package com.fk2droid.protocol;

import java.nio.ByteBuffer;
import java.nio.charset.Charset;

/** Construction des messages envoyes au dongle. */
public final class Messages {
    private static final Charset ASCII = Charset.forName("US-ASCII");
    private static final Charset UTF8 = Charset.forName("UTF-8");

    private Messages() {}

    public static Msg open(DongleConfig c) {
        ByteBuffer b = Msg.le(28);
        b.putInt(c.width);
        b.putInt(c.height);
        b.putInt(c.fps);
        b.putInt(5);        // format : H.264
        b.putInt(49152);    // packetMax
        b.putInt(2);        // iBoxVersion
        b.putInt(2);        // phoneWorkMode
        return new Msg(Msg.OPEN, b.array());
    }

    public static Msg sendFile(String path, byte[] content) {
        byte[] name = (path + "\0").getBytes(ASCII);
        ByteBuffer b = Msg.le(4 + name.length + 4 + content.length);
        b.putInt(name.length);
        b.put(name);
        b.putInt(content.length);
        b.put(content);
        return new Msg(Msg.SEND_FILE, b.array());
    }

    public static Msg sendNumber(String path, int value) {
        return sendFile(path, Msg.le(4).putInt(value).array());
    }

    public static Msg sendString(String path, String value) {
        return sendFile(path, value.getBytes(ASCII));
    }

    public static Msg command(int cmd) {
        return new Msg(Msg.COMMAND, Msg.le(4).putInt(cmd).array());
    }

    public static Msg heartbeat() {
        return new Msg(Msg.HEARTBEAT, null);
    }

    /** x, y normalises entre 0 et 1. */
    public static Msg touch(int action, float x, float y) {
        int ix = clamp((int) (x * 10000f));
        int iy = clamp((int) (y * 10000f));
        ByteBuffer b = Msg.le(16);
        b.putInt(action).putInt(ix).putInt(iy).putInt(0);
        return new Msg(Msg.TOUCH, b.array());
    }

    /**
     * Tactile multipoint : pour chaque doigt x, y (flottants 0..1), action, identifiant.
     * xs/ys normalises entre 0 et 1 ; actions Msg.MT_*.
     */
    public static Msg multiTouch(float[] xs, float[] ys, int[] actions, int[] ids, int count) {
        ByteBuffer b = Msg.le(16 * count);
        for (int i = 0; i < count; i++) {
            b.putFloat(clampF(xs[i]));
            b.putFloat(clampF(ys[i]));
            b.putInt(actions[i]);
            b.putInt(ids[i]);
        }
        return new Msg(Msg.MULTI_TOUCH, b.array());
    }

    /** Active le mode Android Auto du dongle (remis a zero par le dongle apres une deconnexion). */
    public static Msg androidWorkMode(boolean on) {
        return sendNumber("/etc/android_work_mode", on ? 1 : 0);
    }

    /** Parametres complementaires (JSON) attendus par les firmwares recents du dongle. */
    public static Msg boxSettings(DongleConfig c, long epochSeconds) {
        String json = "{\"mediaDelay\":" + c.mediaDelayMs
                + ",\"syncTime\":" + epochSeconds
                + ",\"androidAutoSizeW\":" + c.width
                + ",\"androidAutoSizeH\":" + c.height + "}";
        return new Msg(Msg.BOX_SETTINGS, json.getBytes(UTF8));
    }

    /** Micro : PCM 16 bits, 16 kHz mono (decodeType 5). */
    public static Msg micAudio(short[] pcm, int count) {
        ByteBuffer b = Msg.le(12 + count * 2);
        b.putInt(5);        // decodeType 16 kHz mono
        b.putFloat(0f);     // volume
        b.putInt(3);        // audioType : entree micro
        for (int i = 0; i < count; i++) b.putShort(pcm[i]);
        return new Msg(Msg.AUDIO_DATA, b.array());
    }

    /** Glissement du doigt (fusionnable avec le suivant). */
    public static boolean isTouchMove(Msg m) {
        byte[] p = m.payload;
        if (m.type == Msg.MULTI_TOUCH) {
            // Glissement multipoint : toutes les actions valent MT_MOVE
            if (p.length == 0 || p.length % 16 != 0) return false;
            for (int i = 8; i < p.length; i += 16) {
                if (p[i] != Msg.MT_MOVE || p[i + 1] != 0 || p[i + 2] != 0 || p[i + 3] != 0) return false;
            }
            return true;
        }
        return p.length >= 4 && (p[0] & 0xFF) == Msg.TOUCH_MOVE && p[1] == 0 && p[2] == 0 && p[3] == 0;
    }

    private static float clampF(float v) {
        return v < 0f ? 0f : (v > 1f ? 1f : v);
    }

    private static int clamp(int v) {
        return v < 0 ? 0 : (v > 10000 ? 10000 : v);
    }
}
