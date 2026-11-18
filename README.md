# FK2Droid — Android Auto sur le Honda Connect (Android 4.0.4)

![statut](https://img.shields.io/badge/version-1.0--test2-orange)
![android](https://img.shields.io/badge/Android-4.0.4%20(API%2015)-green)
![licence](https://img.shields.io/badge/licence-MIT-blue)

> [!WARNING]
> **Version 1.0-test2 (18 novembre 2026) — pas encore testée en voiture.** Appli en français ou en anglais selon la langue du Honda. FK2Droid reprend tout le moteur de
> [FK2Play 2.1](https://github.com/jessycloes-oss/fk2play) (validé en voiture : décodage vidéo matériel du Tegra 3,
> tactile, son, appels via le kit mains libres d'origine, touches du volant, arrière-plan) et l'adapte à
> **Android Auto**. Vérifié sur un Honda Connect simulé (Android 4.0.4) avec un faux dongle.
> Vos [rapports de test](../../issues/new?template=rapport-de-test.yml) sont les bienvenus. Installation **à l'arrêt**.

*English version below.*

FK2Droid affiche **Android Auto** sur l'écran d'origine du **Honda Connect** de première génération
(Civic 9ᵉ génération et Civic Type R **FK2**, HR-V, CR-V, Jazz… 2015-2017, Android 4.0.4, NVIDIA Tegra 3),
avec le **même dongle Carlinkit CPC200-CCPA** que FK2Play, mis en mode Android Auto.

```
téléphone Android ──Bluetooth + Wi-Fi 5 GHz──▶ dongle Carlinkit CCPA ──USB──▶ Honda Connect (FK2Droid)
```

## Télécharger

Dernière version : page [**Releases**](../../releases).

| Fichier | Usage |
|---|---|
| `HondaAppCenter_A1.apk` | FK2Droid **déjà renommé** pour l'installateur du Honda Connect (racine d'une clé USB FAT32). |
| `FK2Droid-1.0-test2.apk` | Le même fichier sous son vrai nom. |
| `Mode_emploi_FK2Droid_toutes_versions.pdf` | Mode d'emploi RC3 à RC8 ([docs](docs/)). |
| `Mode_emploi_FK2Droid_RC3.pdf` | Mode d'emploi illustré pour les Honda Connect **RC3** (build `09.08C.00.xxxx`). |
| `User_guide_FK2Droid_all_versions.pdf` · `User_guide_FK2Droid_RC3.pdf` | The same guides in **English**. |

Signé avec la clé de FK2Play — SHA-256 du certificat :
`8D:F7:C2:BD:D0:F1:B9:3E:DF:61:1F:5D:22:06:26:4C:23:65:39:41:EE:7E:39:A9:C8:54:B7:27:D6:CC:29:26`

## Ce qu'il faut

- Un Honda Connect 1ʳᵉ génération sous **Android 4.0.4** et l'outil **Honda Permissions** (S_Mike, XDA, non fourni).
- Un dongle **Carlinkit CPC200-CCPA** (« Autokit »), dont le firmware propose Android Auto.
- Un téléphone **Android 11 ou plus récent** avec Wi-Fi **5 GHz** et l'appli Android Auto à jour.

| Build (Réglages → Android → À propos) | Version | Installation |
|---|---|---|
| `09.08C.00.xxxx` | RC3 | Simple (renommage + Honda Permissions) |
| `0C.091.xx.xxxx` | RC5 | Simple |
| `0E.094.00.xxxx` | RC6 / RC6.1 | Simple |
| `0F.095.01.xxxx` | RC7 | Difficile : retour en RC6 ou iRoot |
| `10.096.00.xxxx` | RC8 | Difficile : retour en RC6 ou iRoot |

**FK2Play et FK2Droid** peuvent être installés ensemble (`com.fk2play` / `com.fk2droid`), mais un seul utilise le dongle à la fois.

## Ce qui change par rapport à FK2Play

- **Mode Android Auto du dongle** : `/etc/android_work_mode = 1` à l'ouverture, renvoyé après chaque déconnexion du téléphone.
- **Mode nuit automatique** selon l'éclairage du Honda (service `StateMgrService`, méthode découverte par MaKi83).
- **Retour sur Android Auto après la caméra de recul.**
- **Densité d'affichage** réglable, **tactile multipoint** en option (message `0x17`).
- **Récupération d'image** : si aucune image clé n'arrive au retour sur l'écran, la session est rouverte (2 fois au plus).
- Diagnostic : *Téléphone vu par le dongle*, *Images clés*, *État du Honda*.

## Compiler

Comme FK2Play : NDK r17c, SDK 34, Gradle 8.14.3.

```
NDK=~/android-ndk-r17c ./scripts/build_native.sh            # FFmpeg + libfk2video.so
ANDROID_SDK=~/android-sdk ./scripts/get_ics_sdk.sh           # en-têtes AOSP 4.0.4 (non publiés)
NDK=~/android-ndk-r17c ./scripts/build_omx.sh                # libfk2omx.so (remettre libfk2video.so après)
./scripts/run_protocol_tests.sh
gradle :app:assembleRelease
```

## Remerciements

**MaKi83** (OpenDroidAuto) pour le décodeur matériel, le service volant et l'état jour / nuit du Honda ;
**S_Mike** pour Honda Permissions ; **node-carplay** / **pycarplay** pour la documentation du protocole.
Voir [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

---

## English

FK2Droid shows **Android Auto** on the stock first-generation **Honda Connect** head unit (Android 4.0.4, Tegra 3)
through a **Carlinkit CPC200-CCPA** dongle switched to Android Auto mode. It is built on FK2Play 2.1 (validated
CarPlay app for the same head unit). **1.0-test is not yet road-tested.** Requirements: Android 11+ phone with
5 GHz Wi-Fi, Honda Permissions (S_Mike, XDA). Install `HondaAppCenter_A1.apk` from a FAT32 USB stick, add a
Process Controls entry for `com.fk2droid` (THIRD_PARTY, NAVI, SoundOut/LastMode ON, SoundInterrupt/
SoundInterruptMute/ProcessKillTarget OFF), plug the dongle, pair the phone with **FK2Droid** over Bluetooth.
The app is in English (French when the head unit is set to French). English guides:
[User_guide_FK2Droid_all_versions.pdf](docs/User_guide_FK2Droid_all_versions.pdf) and
[User_guide_FK2Droid_RC3.pdf](docs/User_guide_FK2Droid_RC3.pdf). Test reports: [form](../../issues/new?template=rapport-de-test.yml).

*Android Auto is a trademark of Google LLC. Not affiliated with Google, Honda or Carlinkit. Use at your own risk.*
