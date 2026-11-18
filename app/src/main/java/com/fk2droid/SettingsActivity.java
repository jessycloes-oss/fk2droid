package com.fk2droid;

import android.os.Bundle;
import android.preference.PreferenceActivity;

/**
 * Reglages (PreferenceActivity : disponible des Android 1.0).
 * Accessible par la touche MENU dans FK2Droid et par sa propre icone « Reglages FK2Droid ».
 */
public class SettingsActivity extends PreferenceActivity {
    @Override
    @SuppressWarnings("deprecation")
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        addPreferencesFromResource(R.xml.preferences);
    }

    @SuppressWarnings("deprecation")
    private void setSummary(String key, String text) {
        android.preference.Preference p = findPreference(key);
        if (p != null && text != null) p.setSummary(text);
    }

    /** Recharge l'ecran au retour du test du micro, qui peut avoir change des reglages. */
    @Override
    @SuppressWarnings("deprecation")
    protected void onResume() {
        super.onResume();
        setPreferenceScreen(null);
        addPreferencesFromResource(R.xml.preferences);
        android.preference.Preference log = findPreference(MediaKeys.PREF_KEY_LOG);
        String keys = getPreferenceManager().getSharedPreferences().getString(MediaKeys.PREF_KEY_LOG, "");
        if (log != null && !keys.isEmpty()) log.setSummary(keys);
        android.preference.Preference vd = findPreference("video_decoder_status");
        if (vd != null) vd.setSummary(com.fk2droid.video.VideoPipeline.decoderDiagnostic());
        setSummary("phone_status", Stats.phoneDiag);
        setSummary("keyframe_status", com.fk2droid.video.VideoPipeline.keyframeDiag);
        AutoService svc = AutoService.get();
        setSummary("honda_state", svc != null && svc.honda() != null ? svc.honda().diagnostic()
                : "FK2Droid n'est pas lance");
        android.preference.Preference sw = findPreference(HondaSteering.PREF_STATUS);
        String st = getPreferenceManager().getSharedPreferences().getString(HondaSteering.PREF_STATUS, "");
        if (sw != null && !st.isEmpty()) sw.setSummary(st);
    }
}
