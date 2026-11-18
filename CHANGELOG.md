# Historique des versions — FK2Droid

## 1.0-test — 18 novembre 2026 (première version, à valider en voiture)

FK2Droid est dérivé de **FK2Play 2.1** (CarPlay, validé en voiture) et affiche **Android Auto** avec le même
dongle Carlinkit CPC200-CCPA. versionCode 1, paquet `com.fk2droid`, signé avec la clé de FK2Play.

- **Mode Android Auto du dongle** : envoi de `/etc/android_work_mode = 1` à l'initialisation (ordre de
  node-carplay) et après chaque `UNPLUGGED` (le dongle l'oublie à la déconnexion du téléphone).
- **Types de téléphone** reconnus : Android Auto (5), CarPlay (3), recopie Android (1) ; filaire / sans fil.
- **Mode nuit** : *Automatique* (état jour / nuit du Honda via `StateMgrService`, lu par réflexion toutes les
  1,5 s), *Toujours jour*, *Toujours nuit* ; changement en direct (commandes 16 / 17), sans rouvrir la session.
- **Caméra de recul** : retour automatique sur Android Auto quand l'écran Honda quitte l'adresse vidéo 92.
  Méthode découverte par MaKi83 (OpenDroidAuto), réimplémentée.
- **Densité d'affichage** (120 à 200 dpi) et **nom Bluetooth** du dongle réglables.
- **Tactile multipoint** (option, message `0x17`, coordonnées flottantes, glissements fusionnés).
- **Image qui ne revient pas** : si aucune image clé n'arrive après 15 demandes avec l'écran affiché, la
  session est rouverte (2 fois au plus). Diagnostic *Images clés* (délai de réponse ou « SANS REPONSE »).
- Diagnostic : *Téléphone vu par le dongle*, *État du Honda (jour / nuit, caméra)*.
- Nouvelle icône verte « FK2 droid ». Textes adaptés (téléphone Android, Assistant Google).
- Tests : 29 tests du protocole (dont mode Android Auto et multipoint) ; essai dans un Honda Connect simulé
  (Android 4.0.4 ARM) avec faux dongle Android Auto : connexion, image, retour depuis l'accueil, réglages,
  tactile multipoint (monkey), sans plantage.

Historique de FK2Play (base de FK2Droid) : https://github.com/jessycloes-oss/fk2play/blob/main/CHANGELOG.md
