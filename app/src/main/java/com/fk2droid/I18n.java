package com.fk2droid;

import java.util.Locale;

/**
 * Messages d'etat et de diagnostic en anglais quand le Honda Connect n'est pas en francais.
 *
 * Le moteur (protocole, journaux) reste en francais ; la traduction se fait seulement a l'affichage,
 * par remplacement de phrases connues (les plus longues d'abord), ce qui couvre aussi les messages
 * composes (« Erreur : … - nouvelle tentative… »). Les reglages, eux, utilisent les ressources Android
 * (values = anglais, values-fr = francais).
 */
public final class I18n {
    private I18n() {}

    /** Ordre important : expressions longues avant leurs morceaux. */
    private static final String[][] PHRASES = {
        // Etat de la connexion
        {"Dongle initialise, en attente du telephone Android...", "Dongle ready, waiting for the Android phone..."},
        {"Branchez le dongle Carlinkit sur le port USB...", "Plug the Carlinkit dongle into the USB port..."},
        {"Autorisez l'acces au dongle USB", "Allow access to the USB dongle"},
        {"Permission USB refusee", "USB permission denied"},
        {"Dongle debranche", "Dongle unplugged"},
        {"Connexion au dongle...", "Connecting to the dongle..."},
        {"Telephone deconnecte - en attente...", "Phone disconnected - waiting..."},
        {"Recopie d'ecran Android connectee", "Android screen mirroring connected"},
        {"CarPlay connecte (iPhone)", "CarPlay connected (iPhone)"},
        {"Android Auto connecte", "Android Auto connected"},
        {"Telephone connecte (type ", "Phone connected (type "},
        {" (sans fil)", " (wireless)"},
        {" (filaire)", " (wired)"},
        {"Pas d'image du telephone : debranchez / rebranchez le dongle", "No picture from the phone: unplug / replug the dongle"},
        {"Image perdue : reconnexion d'Android Auto...", "Picture lost: reconnecting Android Auto..."},
        {" - nouvelle tentative...", " - retrying..."},
        {"Erreur : ", "Error: "},
        {"Firmware dongle : ", "Dongle firmware: "},
        {"Phase dongle : ", "Dongle phase: "},
        {"Appareil : ", "Device: "},
        {"Android Auto actif - toucher pour revenir", "Android Auto running - tap to return"},
        {"USB hote Android : oui", "Android USB host: yes"},
        {"USB hote Android : NON", "Android USB host: NO"},
        {"USB hote Android : ", "Android USB host: "},
        {"aucun peripherique vu", "no device seen"},
        {" | vus : ", " | seen: "},
        {"[USB : ", "[USB: "},
        // Erreurs de transport / protocole
        {"Lecture USB echouee (dongle debranche ?)", "USB read failed (dongle unplugged?)"},
        {"Impossible d'ouvrir le dongle (permission USB ?)", "Cannot open the dongle (USB permission?)"},
        {"Aucune interface bulk trouvee sur le dongle", "No bulk interface found on the dongle"},
        {"claimInterface a echoue", "claimInterface failed"},
        {"Transport ferme", "Transport closed"},
        {"Fin du flux simule (equivaut a un dongle debranche)", "End of simulated stream (same as an unplugged dongle)"},
        {"Magic invalide: ", "Invalid magic: "},
        {"Controle de type invalide pour type ", "Invalid type check for type "},
        {"Longueur invalide: ", "Invalid length: "},
        {"En-tete trop court", "Header too short"},
        // Diagnostic
        {"aucun depuis le demarrage", "none since start"},
        {"aucune demande pour l'instant", "no request yet"},
        {"OK : image cle recue en ", "OK: key frame received in "},
        {" relance(s))", " retry(ies))"},
        {"SANS REPONSE apres ", "NO ANSWER after "},
        {" demandes (", " requests ("},
        {"service absent (pas un Honda Connect ?)", "service missing (not a Honda Connect?)"},
        {"introuvable (pas un Honda Connect ?)", "not found (not a Honda Connect?)"},
        {"pas encore lu", "not read yet"},
        {"aucun etat", "no state"},
        {"erreur de lecture : ", "read error: "},
        {", ecran Honda ", ", Honda screen "},
        {" (camera de recul)", " (reverse camera)"},
        {"FK2Droid n'est pas lance", "FK2Droid is not running"},
        {"aucun pour l'instant (afficher Android Auto une fois)", "none yet (show Android Auto once)"},
        {"Materiel desactive dans les reglages", "Hardware disabled in settings"},
        {"Dernier utilise (il y a ", "Last used ("},
        {" min) : ", " min ago): "},
        {" s) : ", " s ago): "},
        {"En cours : ", "Running: "},
        {"Materiel : ", "Hardware: "},
        {"FFmpeg (logiciel)", "FFmpeg (software)"},
        {"Logiciel : ", "Software: "},
        {"aucun decodeur H.264 materiel sur cet autoradio", "no H.264 hardware decoder on this head unit"},
        {"le decodeur materiel ne repond plus", "the hardware decoder stopped responding"},
        {"aucune image affichee par le decodeur materiel", "no picture shown by the hardware decoder"},
        {"bibliotheque non chargee (", "library not loaded ("},
        {"erreur a l'initialisation : ", "initialisation error: "},
        {"Aucun decodeur video disponible !", "No video decoder available!"},
        {"Decodeur materiel indisponible : retour au logiciel", "Hardware decoder unavailable: back to software"},
        {" images affichees", " frames shown"},
        {" images, ", " frames, "},
        {" jetees", " dropped"},
        {"connecte (adresse ", "connected (address "},
        {", mode ", ", mode "},
        {"erreur d'inscription : ", "registration error: "},
        {"rendue impossible : ", "could not be handed back: "},
        {"rendue au Honda", "handed to the Honda"},
        {"rendu au Honda", "handed to the Honda"},
        {"touche volume", "volume key"},
        {"Aucune pour l'instant", "None yet"},
        {"Touche ", "Key "},
        {" precedent ", " previous "},
        {" suivant ", " next "},
        {" (ignoree)", " (ignored)"},
        {"jour", "day"},
        {"nuit", "night"},
        // Test du micro
        {"Test du micro de la voiture", "Car microphone test"},
        {"Lancer le test du micro", "Start the microphone test"},
        {"Relancer le test", "Run the test again"},
        {"PARLEZ MAINTENANT, sans arreter... (environ 20 secondes)", "TALK NOW, without stopping... (about 20 seconds)"},
        {"bloque (aucune donnee)", "blocked (no data)"},
        {" (silence total)", " (total silence)"},
        {"% des donnees", "% of data"},
        {"niveau ", "level "},
    };

    private static volatile Boolean english;

    /** Anglais pour toute langue autre que le francais. */
    public static boolean english() {
        Boolean e = english;
        if (e == null) {
            e = !"fr".equals(Locale.getDefault().getLanguage());
            english = e;
        }
        return e;
    }

    /** Traduit un message d'affichage (sans effet en francais). */
    public static String t(String fr) {
        if (fr == null || !english()) return fr;
        String s = fr;
        for (String[] p : PHRASES) {
            if (s.contains(p[0])) s = s.replace(p[0], p[1]);
        }
        return s;
    }

    /** Choix direct d'un texte long (le test du micro). */
    public static String pick(String fr, String en) {
        return english() ? en : fr;
    }
}
