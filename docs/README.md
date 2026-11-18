# Modes d'emploi FK2Droid 1.0-test

> [!WARNING]
> **Version d'essai**, pas encore testée en voiture. Vos [rapports de test](../../../issues/new?template=rapport-de-test.yml) sont les bienvenus.

| Guide | Pour qui |
|---|---|
| [Mode_emploi_FK2Droid_RC3.pdf](Mode_emploi_FK2Droid_RC3.pdf) | Honda Connect **RC3** (build `09.08C.00.xxxx`) : guide pas à pas illustré. |
| [Mode_emploi_FK2Droid_toutes_versions.pdf](Mode_emploi_FK2Droid_toutes_versions.pdf) | Toutes versions (RC3 à RC8), avec les chemins RC7 / RC8. |

Les PDF sont générés par `source/gen.py` (HTML → PDF avec Chrome sans interface, puis `source/footer.py`
pour les numéros de page).

## Résumé (RC3 à RC6.1)

1. **Version** : HOME → Réglages → Android → À propos du dispositif → *Numéro de build*.
2. **Honda Permissions** (S_Mike, XDA, non fourni ici) — déjà en place si FK2Play est installé.
3. **Installer FK2Droid** : `HondaAppCenter_A1.apk` de la [release](../../../releases), seul à la racine d'une clé USB FAT32.
4. **Droits** : Honda Permissions → *Process Controls* → `+` : `com.fk2droid`, `THIRD_PARTY`, `NAVI`, SoundOut / LastMode **ON** ; SoundInterrupt / SoundInterruptMute / ProcessKillTarget **OFF**.
5. **Brancher le dongle** CPC200-CCPA : « Dongle initialise, en attente du telephone Android... ».
6. **Téléphone** (Android 11+, Wi-Fi 5 GHz) : associer **FK2Droid** en Bluetooth, accepter Android Auto.
7. **Appels** : téléphone connecté à HandsFreeLink + *Appels via le Bluetooth de la voiture*.
