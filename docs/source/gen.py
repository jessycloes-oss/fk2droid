#!/usr/bin/env python3
"""Genere les deux modes d'emploi FK2Droid (RC3 illustre + toutes versions) en HTML, puis PDF via Chrome."""
import os, sys

VER = "1.0-test2"
DATE = "18 novembre 2026"
HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
@page { size: A4; margin: 14mm 14mm 16mm 14mm; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 10.4pt; line-height: 1.42; color: #1d2329; margin: 0; }
h1 { font-size: 21pt; margin: 0 0 2mm 0; color: #14633f; }
h2 { font-size: 14pt; margin: 6mm 0 2mm 0; color: #14633f; border-bottom: 2px solid #2eaa64; padding-bottom: 1mm; page-break-after: avoid; }
h3 { font-size: 11.5pt; margin: 4mm 0 1.5mm 0; color: #1d2329; page-break-after: avoid; }
.sub { color: #55606b; font-size: 9.6pt; margin-bottom: 4mm; }
.box { border-radius: 2mm; padding: 2.5mm 3.5mm; margin: 3mm 0; page-break-inside: avoid; }
.ok { background: #e7f6ee; border-left: 4px solid #2eaa64; }
.warn { background: #fff4e0; border-left: 4px solid #e69500; }
.stop { background: #fdeaea; border-left: 4px solid #c62828; }
.info { background: #eef3f8; border-left: 4px solid #4a78a8; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 3mm 0; page-break-inside: avoid; font-size: 9.8pt; }
th { background: #14633f; color: white; text-align: left; padding: 1.6mm 2mm; font-weight: bold; }
td { border-bottom: 1px solid #d5dbe0; padding: 1.5mm 2mm; vertical-align: top; }
tr:nth-child(even) td { background: #f6f8f9; }
code, .ui { font-family: 'DejaVu Sans Mono', monospace; font-size: 9.2pt; background: #eef1f3; padding: 0.2mm 1.2mm; border-radius: 1mm; }
b.menu { color: #14633f; }
ol, ul { margin: 1mm 0 2mm 0; padding-left: 6mm; }
li { margin: 0.6mm 0; }
.pb { page-break-before: always; }
.cols { display: flex; gap: 5mm; align-items: flex-start; }
.cols > div { flex: 1; }
figure { margin: 0; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; border: 1px solid #c8cfd5; border-radius: 1.5mm; }
figcaption { font-size: 8.6pt; color: #55606b; margin-top: 1mm; }
.diagram { display: flex; align-items: center; justify-content: space-between; gap: 2mm; margin: 4mm 0; }
.node { border: 2px solid #2eaa64; border-radius: 3mm; padding: 3mm; text-align: center; font-size: 9.4pt; flex: 1; background: #f3fbf6; }
.node b { display: block; font-size: 10.5pt; color: #14633f; }
.arrow { font-size: 8.6pt; color: #55606b; text-align: center; min-width: 22mm; }
.toc { columns: 2; font-size: 9.8pt; }
.check td:first-child { width: 42%; }
.small { font-size: 8.8pt; color: #55606b; }
.step { display: flex; gap: 3mm; margin: 1.6mm 0; }
.num { background: #2eaa64; color: white; border-radius: 50%; width: 6.5mm; height: 6.5mm; min-width: 6.5mm; text-align: center; line-height: 6.5mm; font-weight: bold; font-size: 9.5pt; }
.foot { position: fixed; bottom: -9mm; left: 0; right: 0; text-align: center; font-size: 8pt; color: #7a858f; }
"""

def html(title, body):
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{title}</title>
<style>{CSS}</style></head><body>
{body}</body></html>"""

def step(n, text):
    return f'<div class="step"><div class="num">{n}</div><div>{text}</div></div>'

# ---------------------------------------------------------------- blocs communs

def nouveautes():
    return f"""
<h1>FK2Droid {VER} — à lire d'abord</h1>
<div class="sub">Android Auto sur le Honda Connect · première version d'essai · {DATE}</div>

<div class="box warn"><b>Version d'essai, pas encore testée en voiture.</b> FK2Droid reprend tout le moteur de
<b>FK2Play 2.1</b> (validé en voiture : image décodée par le Tegra 3, tactile, son, appels par le kit mains libres,
touches du volant, arrière-plan). La partie Android Auto a été vérifiée dans un Honda Connect simulé (Android 4.0.4),
pas encore en voiture : tes retours décideront de la 1.0.</div>

<p><b>En une phrase :</b> c'est FK2Play, mais pour les téléphones <b>Android</b> : le même dongle Carlinkit CPC200-CCPA est mis en mode
<b>Android Auto</b>, et FK2Droid affiche Android Auto sur l'écran 7" du Honda Connect, comme FK2Play affiche CarPlay.</p>

<h3>Ce qui est nouveau par rapport à FK2Play</h3>
<table style="font-size:8.4pt">
<tr><th style="width:32%">Fonction</th><th>Détail</th></tr>
<tr><td>Mode Android Auto du dongle</td><td>FK2Droid envoie au dongle le réglage <code>android_work_mode = 1</code> à chaque
connexion, et le renvoie après chaque déconnexion du téléphone (le dongle l'oublie).</td></tr>
<tr><td>Mode nuit automatique</td><td>Suit l'éclairage du Honda (phares allumés → carte Google Maps sombre). Lecture du
service d'état du Honda Connect, méthode découverte par MaKi83 (OpenDroidAuto).</td></tr>
<tr><td>Retour après la caméra de recul</td><td>Si Android Auto était affiché quand tu passes la marche arrière,
FK2Droid revient tout seul sur Android Auto quand la caméra s'éteint.</td></tr>
<tr><td>Taille de l'affichage</td><td>Réglage de la densité envoyée au téléphone (boutons plus ou moins gros).</td></tr>
<tr><td>Tactile multipoint (option)</td><td>Pincer pour zoomer dans Google Maps. Décoché par défaut : à essayer.</td></tr>
<tr><td>Image qui ne revient pas</td><td>Si le téléphone ne renvoie pas d'image au retour sur FK2Droid, la connexion est
rouverte automatiquement (2 fois au plus). Une ligne de diagnostic indique si c'est arrivé.</td></tr>
<tr><td>Nom Bluetooth · langue</td><td>Le dongle s'annonce <b>FK2Droid</b> (modifiable). L'appli est en français, ou en anglais
si le Honda Connect est réglé dans une autre langue (depuis la 1.0-test2).</td></tr>
</table>

<h3>À tester en voiture, dans cet ordre</h3>
<ol style="font-size:9.1pt">
<li>Le téléphone Android se connecte et Android Auto s'affiche (message <span class="ui">Android Auto connecte (sans fil)</span>).</li>
<li>Tactile, musique, voix du GPS, touches piste du volant.</li>
<li>Quitter FK2Droid (radio, réglages) puis revenir : l'image doit revenir en moins de 2 secondes.</li>
<li>Un appel (avec l'option « Appels via le Bluetooth de la voiture »).</li>
<li>Allumer les phares : la carte passe en mode sombre en quelques secondes.</li>
<li>Marche arrière depuis l'écran Android Auto, puis marche avant : retour automatique sur Android Auto.</li>
</ol>
<p>Ensuite, photographie <b class="menu">Réglages FK2Droid › Diagnostic</b> : lignes <i>Téléphone vu par le dongle</i>,
<i>Images clés</i>, <i>État du Honda</i> et <i>Décodeur vidéo actif</i>.</p>

<div class="box info" style="font-size:8.9pt"><b>Tu as déjà FK2Play ?</b> FK2Droid s'installe <b>à côté</b>
(paquet <code>com.fk2droid</code>, même dongle, même clé). Va directement à « Installer FK2Droid ». Une seule des deux
applis utilise le dongle à la fois.</div>

"""

def schema():
    return """
<div class="diagram">
  <div class="node"><b>Téléphone Android</b>Android 11 ou plus<br>appli Android Auto</div>
  <div class="arrow">Bluetooth + Wi-Fi 5 GHz<br>⇢ ⇢ ⇢<br>(sans fil)</div>
  <div class="node"><b>Dongle Carlinkit CPC200-CCPA</b>le même que pour FK2Play<br>mis en mode Android Auto</div>
  <div class="arrow">câble USB<br>image, son ⇢<br>⇠ tactile, touches</div>
  <div class="node"><b>Honda Connect</b>Android 4.0.4<br>FK2Droid affiche Android Auto</div>
</div>
<p>Le Honda Connect est trop ancien pour faire tourner Android Auto lui-même (Android Auto pour autoradio demande
une puissance et un système bien plus récents). Le dongle s'occupe de toute la partie Google : FK2Droid reçoit
l'image (vidéo H.264), la décode avec la puce vidéo du Tegra 3, joue le son et renvoie le tactile et les touches.</p>
"""

def besoin(rc3):
    honda = ("<tr><td>Honda Permissions (S_Mike)</td><td>Déjà installé si tu utilises FK2Play. Sinon : forum XDA, fil "
             "« Honda Connect Android System », ou cmdroid.com (non fourni ici, outil d'un autre auteur).</td></tr>")
    return f"""
<table>
<tr><th style="width:30%">Élément</th><th>Détail</th></tr>
<tr><td>Dongle Carlinkit CPC200-CCPA</td><td>Le modèle « Autokit » pour autoradio Android, <b>le même que pour FK2Play</b>
(USB <code>1314:1520</code> ou <code>1314:1521</code>). Pas un 5.0 / 2Air / U2W / Mini. Version CCPA-MIC (micro intégré)
conseillée si tu veux parler à l'Assistant Google (le micro de la voiture n'est pas accessible aux applis).</td></tr>
<tr><td>Téléphone Android</td><td><b>Android 11 ou plus récent</b>, Wi-Fi <b>5 GHz</b>, appli <b>Android Auto</b> à jour
(Play Store), données mobiles actives. Google exige Android 11 et le Wi-Fi 5 GHz pour Android Auto sans fil.</td></tr>
<tr><td>FK2Droid</td><td><code>HondaAppCenter_A1.apk</code> (= FK2Droid déjà renommé, prêt à copier) ou
<code>FK2Droid-{VER}.apk</code>, dans le dossier <code>fk2droid</code>.</td></tr>
<tr><td>Clé USB</td><td>FAT32, 32 Go maximum, vide de préférence.</td></tr>
{honda}
<tr><td>Ce mode d'emploi</td><td>Imprimé ou sur une tablette, avec la fiche de résultats (dernière page).</td></tr>
</table>
<div class="box warn"><b>Firmware du dongle.</b> Selon les vendeurs, le CPC200-CCPA fait Android Auto sans fil avec les
firmwares récents, et seulement CarPlay (ou Android Auto filaire) avec certains anciens. <b>Commence sans rien mettre
à jour</b> : FK2Droid affiche <span class="ui">Firmware dongle : …</span> au branchement, note-le dans la fiche. Une mise à
jour du firmware n'est à envisager que si Android Auto n'apparaît jamais (voir Dépannage), car elle peut changer le
comportement du dongle avec FK2Play.</div>
"""

VERSIONS = """
<table>
<tr><th>Numéro de build affiché</th><th>Version</th><th>Android</th><th>Installation de Honda Permissions</th><th>FK2Droid</th></tr>
<tr><td><code>09.08C.00.xxxx</code><br><span class="small">ex. 09.08C.00.1123, 09.08C.00.0021</span></td><td><b>RC3</b></td><td>4.0.4</td><td>Simple : astuce du renommage (étape 3A) — guide illustré RC3</td><td>✔ cible principale</td></tr>
<tr><td><code>0C.091.xx.xxxx</code></td><td><b>RC5</b></td><td>4.0.4</td><td>Simple (étape 3A)</td><td>✔ prévu, à confirmer</td></tr>
<tr><td><code>0E.094.00.xxxx</code></td><td><b>RC6 / RC6.1</b></td><td>4.0.4</td><td>Simple (étape 3A)</td><td>✔ prévu, à confirmer</td></tr>
<tr><td><code>0F.095.01.xxxx</code></td><td><b>RC7</b></td><td>4.0.4</td><td>Difficile : retour en RC6 ou iRoot (étape 3B)</td><td>✔ une fois Honda Permissions en place</td></tr>
<tr><td><code>10.096.00.xxxx</code> (ou 10.96…)</td><td><b>RC8</b></td><td>4.0.4</td><td>Difficile (étape 3B)</td><td>✔ une fois Honda Permissions en place</td></tr>
</table>
<p class="small">Numéros relevés sur le forum XDA (fil « Honda Connect Android System ») et vérifiés pour la RC3 sur la
Civic Type R FK2 du développeur. FK2Droid ne dépend pas de la RC : seules l'installation de Honda Permissions et le
blocage des installations changent d'une version à l'autre. Le service volant et l'état jour / nuit du Honda ont été
relevés en RC3 ; sur les autres RC, s'ils ne répondent pas, FK2Droid fonctionne quand même (les lignes de diagnostic
l'indiqueront).</p>
"""

def lire_build(rc3):
    img = ("""<div class="cols"><div>""" if rc3 else "<div><div>")
    t = f"""
{img}
<ol>
<li>Sur l'autoradio : <b class="menu">HOME → Réglages → Android → À propos du dispositif</b>.</li>
<li>Lis la ligne <b>Numéro de build</b> et recopie-la dans la fiche de résultats.</li>
<li>Repère ta version dans le tableau ci-dessous : il te dit quel chemin suivre.</li>
</ol>
</div>"""
    if rc3:
        t += """<div><figure><img src="img/exemple-version-rc3.jpg" style="max-height:52mm">
<figcaption>Honda Connect RC3 réel : build 09.08C.00.1123, Android 4.0.4, noyau 3.1.10.</figcaption></figure></div>"""
    t += "</div>" + VERSIONS
    return t

def honda_perms(rc3):
    a = """
<h3>3A. Versions RC3 à RC6.1 (astuce du renommage)</h3>
<ol>
<li>Sur le PC, renomme le fichier Honda Permissions en <code>HondaAppCenter_A1.apk</code> et copie-le seul à la racine de
la clé USB. Sous Windows, active <i>Affichage → Extensions de noms de fichiers</i> pour éviter un
<code>HondaAppCenter_A1.apk.apk</code>.</li>
<li>Dans la voiture, branche la clé, ouvre l'installateur d'APK (<i>Install apk</i>), choisis le fichier et touche <b>Installer</b>.</li>
<li>Si l'installation est refusée : réinitialisation usine d'Android (<b class="menu">HOME → Réglages → Android →
Sauvegarder et réinitialiser</b>), refuse toute mise à jour d'applis Honda, puis recommence. Cela efface les
téléphones appairés et les applis ajoutées.</li>
<li>Ouvre Honda Permissions → <b>Allowed Installations</b>. Appui long sur <code>HondaAppCenter_A1.apk</code> → crayon →
<b>Sig digest sha256</b> = <code>PREINSTALL</code> → enregistre. <b>Ne supprime jamais cette ligne.</b></li>
<li>Fais une sauvegarde de Honda Permissions sur la clé (fonction backup).</li>
</ol>
"""
    b = """
<h3>3B. Versions RC7 et RC8</h3>
<div class="box stop">L'astuce du renommage est bloquée à partir de la RC7. Deux voies existent sur XDA, toutes deux
plus risquées : <b>revenir en RC6</b> avec les fichiers partagés sur le forum puis faire l'étape 3A, ou <b>iRoot</b> pour
injecter Honda Permissions. Un retour de RC6 vers RC8 a provoqué chez un utilisateur un redémarrage en boucle :
lis bien le fil XDA avant de toucher au firmware, et demande de l'aide en cas de doute.</div>
"""
    if rc3:
        return ("""<div class="box ok"><b>Tu es en RC3 :</b> c'est le cas le plus simple, pas besoin de changer de firmware ni
de rooter. <b>Si Honda Permissions est déjà installé (tu utilises FK2Play), saute cette étape.</b></div>""" + a)
    return ("""<div class="box ok">Si l'icône Honda Permissions est déjà présente (par exemple parce que FK2Play est installé),
saute directement à l'étape 4.</div>""" + a + b)

def installer(rc3):
    return f"""
<ol>
<li>Sur le PC, vide la clé, puis copie <code>HondaAppCenter_A1.apk</code> du dossier <code>fk2droid</code> à sa racine.
<b>C'est bien FK2Droid</b> (même nom de fichier que pour FK2Play : c'est le nom qu'accepte le Honda).</li>
<li>Dans la voiture, branche la clé → installateur d'APK → <code>HondaAppCenter_A1.apk</code> → <b>Installer</b>.</li>
<li>Retire la clé. Deux icônes apparaissent : <b>FK2Droid</b> (carré vert « FK2 droid ») et <b>Réglages FK2Droid</b>.
FK2Play, s'il est installé, reste là et n'est pas modifié.</li>
</ol>
<div class="box info"><b>Bouton Installer grisé ?</b> Dans Honda Permissions → Allowed Installations, touche +, puis
<i>APK Name</i> <code>application.apk</code>, <i>Package name</i> vide, <i>Sig digest</i> <code>PREINSTALL</code>. Copie alors
<code>FK2Droid-{VER}.apk</code> renommé en <code>application.apk</code>.</div>
<p class="small">Mise à jour plus tard : même méthode avec le nouveau <code>HondaAppCenter_A1.apk</code>. FK2Droid se met à
jour et garde ses réglages. Ferme toujours FK2Droid avant (débranche le dongle).</p>
"""

PROCESS = """
<table>
<tr><th style="width:42%">Champ</th><th>Valeur</th></tr>
<tr><td>Process name</td><td><code>com.fk2droid</code></td></tr>
<tr><td>Package name</td><td><code>com.fk2droid</code></td></tr>
<tr><td>Auth Type</td><td>THIRD_PARTY</td></tr>
<tr><td>App Type</td><td>NAVI (Android Auto sert surtout au GPS)</td></tr>
<tr><td>SoundOut · LastMode</td><td>☑ ON</td></tr>
<tr><td>SoundInterrupt · SoundInterruptMute</td><td>☐ <b>OFF</b> (sinon le volume au volant ne répond plus)</td></tr>
<tr><td>VideoOut · OomSetPerm</td><td>☐ OFF</td></tr>
<tr><td>ProcessKillTarget</td><td>☐ OFF (évite que le Honda ferme FK2Droid)</td></tr>
</table>
"""

def droits():
    return f"""
<p>Sans cette étape, le Honda Connect peut couper le son de FK2Droid ou fermer l'appli en roulant.</p>
<ol>
<li>Ouvre Honda Permissions → <b>Process Controls</b> → <b>+</b>.</li>
<li>Remplis comme ci-dessous (mêmes valeurs que la ligne <code>com.fk2play</code> validée le 15 novembre 2026, seul le nom change).</li>
<li>Enregistre, puis refais une sauvegarde sur la clé.</li>
</ol>
{PROCESS}
"""

def cohabitation():
    return """
<p>FK2Play (iPhone, CarPlay) et FK2Droid (Android, Android Auto) peuvent rester installés tous les deux, mais
<b>un seul peut utiliser le dongle à la fois</b>.</p>
<ul>
<li><b>Au branchement du dongle</b>, Android demande quelle appli ouvrir. Si tu avais coché <i>Utiliser par défaut</i>
pour FK2Play, c'est lui qui s'ouvre tout seul : pour pouvoir choisir, va dans <b class="menu">Réglages → Applications →
FK2Play → Effacer les valeurs par défaut</b>.</li>
<li><b>Une seule personne, un seul téléphone</b> : coche <i>Utiliser par défaut</i> pour la bonne appli.</li>
<li><b>iPhone et Android dans le foyer</b> : ne coche pas <i>Utiliser par défaut</i> ; la question s'affiche à chaque
démarrage et tu choisis.</li>
<li><b>Changer d'appli</b> : débranche le dongle 5 secondes, rebranche-le et choisis l'autre appli. Ne lance pas l'une
pendant que l'autre affiche déjà son écran.</li>
</ul>
<div class="box info">Un iPhone branché sur FK2Droid n'est pas le but de l'appli, mais FK2Droid sait reconnaître CarPlay
(message <span class="ui">CarPlay connecte (iPhone)</span>). Pour l'iPhone, garde FK2Play, qui est validé.</div>
"""

def test1():
    return """
<ol>
<li>Lance <b>FK2Droid</b>. L'écran devient noir avec un message au centre.</li>
<li>Recopie la ligne entre crochets, par exemple <span class="ui">[USB hote Android : oui | aucun peripherique vu]</span>.</li>
</ol>
<table><tr><th>Ligne affichée</th><th>Signification</th></tr>
<tr><td><span class="ui">USB hote Android : oui</span></td><td>Bon signe : continue.</td></tr>
<tr><td><span class="ui">USB hote Android : NON</span></td><td>Continue quand même : le test 2 tranchera.</td></tr></table>
"""

def test2():
    return """
<ol>
<li>FK2Droid restant ouvert, branche le dongle <b>directement</b> sur le port USB de la console (pas de hub).</li>
<li>Si Android demande « Autoriser FK2Droid à accéder au périphérique USB ? », touche <b>OK</b> (voir « FK2Play et
FK2Droid ensemble » pour la case <i>Utiliser par défaut</i>).</li>
<li>Attends 5 à 10 secondes et note ce qui s'affiche :</li>
</ol>
<table><tr><th style="width:45%">Message</th><th>Signification et suite</th></tr>
<tr><td><span class="ui">Dongle initialise, en attente du telephone Android...</span> et/ou <span class="ui">Firmware dongle : 20xx...</span></td>
<td>✔ L'autoradio pilote le dongle et l'a mis en mode Android Auto. Note le firmware, passe au test 3.</td></tr>
<tr><td><span class="ui">Branchez le dongle...</span> avec <span class="ui">vus : 1314:1520</span> ou <span class="ui">1314:1521</span></td>
<td>Dongle vu mais pas ouvert. Vérifie que FK2Play ne tourne pas (débranche / rebranche), relance FK2Droid une fois.</td></tr>
<tr><td><span class="ui">vus : xxxx:yyyy</span> (autre numéro)</td><td>Autre modèle de dongle : signale ce numéro.</td></tr>
<tr><td><span class="ui">Autorisez l'acces au dongle USB</span> qui reste affiché</td><td>Débranche le dongle, rebranche-le, accepte la fenêtre.</td></tr>
<tr><td><span class="ui">Erreur : ... nouvelle tentative...</span> en boucle</td><td>Recopie le texte exact de l'erreur.</td></tr>
</table>
"""

def test3(rc3):
    img = ""
    if os.path.exists(os.path.join(HERE, "img", "fk2droid-connecte.png")):
        img = """<figure style="margin:2mm 0"><img src="img/fk2droid-connecte.png" style="max-height:48mm">
<figcaption>Capture réelle de FK2Droid dans un Honda Connect simulé (Android 4.0.4) avec un faux dongle en mode
Android Auto : une mire de test remplace l'écran Android Auto.</figcaption></figure>"""
    return f"""
<h3>Préparer le téléphone (une seule fois)</h3>
<ol>
<li>Mets à jour <b>Android Auto</b> (Play Store) et les services Google Play. Active Wi-Fi, Bluetooth et données mobiles.</li>
<li><b>Appels</b> (le micro de la voiture n'est pas accessible aux applis) : garde le téléphone connecté à
<b>HandsFreeLink</b>, le Bluetooth d'origine du Honda, et coche <b class="menu">Réglages FK2Droid → Audio → Appels via le
Bluetooth de la voiture</b>. La musique reste en USB ; le Honda prend chaque appel avec son micro et les touches du
volant, puis FK2Droid revient sur Android Auto.</li>
</ol>
<h3>Première connexion</h3>
{step(1, "Sur le téléphone : <b>Paramètres → Appareils connectés → Associer un nouvel appareil</b>, choisis <b>FK2Droid</b> (ou <code>AutoKit-xxxx</code> selon le firmware du dongle). Accepte le code d'association.")}
{step(2, "Le téléphone propose Android Auto : accepte toutes les demandes (autorisations, « Utiliser Android Auto avec ce véhicule ? »). <b>Déverrouille le téléphone</b> lors de la première fois.")}
{step(3, "Le dongle bascule tout seul le téléphone en Wi-Fi 5 GHz. Après 10 à 40 secondes, Android Auto s'affiche sur le Honda et FK2Droid indique brièvement <span class='ui'>Android Auto connecte (sans fil)</span>.")}
{step(4, "Essaie et coche dans la fiche : tactile, musique, voix du GPS, un appel, touches du volant, mode nuit, caméra de recul.")}
{img}
<p>Les fois suivantes, la connexion est automatique au démarrage de la voiture, téléphone dans la poche.</p>
<table><tr><th style="width:45%">Ce que tu vois</th><th>Ce que ça veut dire</th></tr>
<tr><td><span class="ui">Android Auto connecte (sans fil)</span></td><td>✔ Tout est bon.</td></tr>
<tr><td><span class="ui">Android Auto connecte (filaire)</span></td><td>✔ Le dongle fait Android Auto par câble (selon firmware).</td></tr>
<tr><td><span class="ui">CarPlay connecte (iPhone)</span></td><td>C'est un iPhone qui s'est connecté : utilise FK2Play.</td></tr>
<tr><td><span class="ui">Recopie d'ecran Android connectee</span></td><td>Le dongle n'est pas passé en Android Auto : débranche / rebranche le dongle ; si ça persiste, voir Dépannage (firmware).</td></tr>
<tr><td>Le téléphone n'apparaît pas / ne propose jamais Android Auto</td><td>Voir Dépannage.</td></tr>
</table>
"""

def reglages():
    img = ""
    if os.path.exists(os.path.join(HERE, "img", "fk2droid-reglages.png")):
        img = """<figure style="margin:2mm 0 3mm 0"><img src="img/fk2droid-reglages.png" style="max-height:56mm">
<figcaption>Écran réel des réglages de FK2Droid (Android 4.0.4 simulé).</figcaption></figure>"""
    if os.path.exists(os.path.join(HERE, "img", "fk2droid-diagnostic.png")):
        img = ('<div class="cols"><div>' + img + '</div><div><figure style="margin:2mm 0 3mm 0">'
               '<img src="img/fk2droid-diagnostic.png" style="max-height:56mm"><figcaption>Lignes de diagnostic propres '
               'à FK2Droid, après une connexion simulée et un retour depuis l\'accueil.</figcaption></figure></div></div>')
    return f"""
<p>Icône <b>Réglages FK2Droid</b> dans la liste des applis, touche MENU de l'autoradio, ou appui long sur le message d'état.
Les réglages qui concernent le dongle s'appliquent au retour sur FK2Droid (reconnexion de quelques secondes).</p>
{img}
<table>
<tr><th style="width:38%">Réglage</th><th style="width:16%">Par défaut</th><th>À quoi il sert</th></tr>
<tr><td>Vidéo › Résolution / Images par seconde</td><td>800x480 · 30</td><td>Baisse-les si l'image saccade.</td></tr>
<tr><td>Vidéo › Décodeur vidéo</td><td>Automatique</td><td>Puce vidéo du Tegra 3, repli sur le logiciel. « Logiciel uniquement » en secours.</td></tr>
<tr><td>Vidéo › <b>Mode nuit Android Auto</b></td><td>Automatique</td><td>Suit l'éclairage du Honda. « Toujours jour » / « Toujours nuit » si tu préfères.</td></tr>
<tr><td>Vidéo › <b>Taille de l'affichage</b></td><td>160</td><td>Densité envoyée au téléphone : 120 = plus d'informations, 200 = boutons plus gros.</td></tr>
<tr><td>Vidéo › <b>Tactile multipoint</b></td><td>décoché</td><td>Pincer pour zoomer dans Maps. Décoche si le tactile réagit mal.</td></tr>
<tr><td>Audio › Touches musique du volant</td><td>coché</td><td>Piste suivante / précédente au volant quand Android Auto est affiché.</td></tr>
<tr><td>Audio › Appels via le Bluetooth de la voiture</td><td>décoché</td><td><b>À cocher</b> sur Honda Connect (voir test 3).</td></tr>
<tr><td>Audio › <b>Revenir à Android Auto après la caméra de recul</b></td><td>coché</td><td>Retour automatique après la marche arrière.</td></tr>
<tr><td>Audio › Revenir à Android Auto dès la fin d'un appel</td><td>coché</td><td>Sans attendre que le Honda quitte son écran téléphone.</td></tr>
<tr><td>Audio › Son Android Auto via l'autoradio (USB)</td><td>coché</td><td>Décoche pour faire passer le son par le Bluetooth.</td></tr>
<tr><td>Connexion › <b>Nom Bluetooth du dongle</b></td><td>FK2Droid</td><td>Nom visible sur le téléphone (16 caractères au plus).</td></tr>
<tr><td>Connexion › Wi-Fi 5 GHz</td><td>coché</td><td>Laisse coché : Android Auto sans fil exige le 5 GHz.</td></tr>
<tr><td>Diagnostic › <b>Téléphone vu par le dongle</b></td><td>—</td><td>Type de connexion reçu (Android Auto, CarPlay, recopie) et heure.</td></tr>
<tr><td>Diagnostic › <b>Images clés</b></td><td>—</td><td>« OK : image clé reçue en … ms » ou « SANS REPONSE » : dit si le retour sur Android Auto est instantané.</td></tr>
<tr><td>Diagnostic › <b>Relancer si l'image ne revient pas</b></td><td>coché</td><td>Rouvre la connexion si l'écran reste noir au retour.</td></tr>
<tr><td>Diagnostic › <b>État du Honda</b></td><td>—</td><td>« jour / nuit, écran Honda N » : vérifie la lecture des phares et de la caméra.</td></tr>
<tr><td>Diagnostic › Décodeur vidéo actif · Service volant Honda · Dernières touches reçues</td><td>—</td><td>Comme dans FK2Play 2.1.</td></tr>
</table>

<h3>Touches du volant (comme FK2Play 2.0)</h3>
<table><tr><th>Touche</th><th>Sur l'écran Android Auto</th><th>Ailleurs</th></tr>
<tr><td>Piste suivante / précédente</td><td>Morceau suivant / précédent</td><td>Fonction Honda habituelle</td></tr>
<tr><td>Volume + / −</td><td>Volume du Honda (affiché au tableau de bord)</td><td>Idem</td></tr>
<tr><td>Raccrocher (pendant un appel)</td><td>Raccroche</td><td>Kit mains libres d'origine</td></tr></table>
<p><b>Android Auto reste actif en arrière-plan</b> : tu peux aller sur la radio ou dans les réglages, la musique, le
guidage vocal et la connexion continuent. Pour revenir, touche l'icône FK2Droid ou sa notification.</p>
"""

def depannage():
    return """
<table>
<tr><th style="width:34%">Problème</th><th>À essayer</th></tr>
<tr><td>Le téléphone ne voit pas <b>FK2Droid</b> en Bluetooth</td><td>Vérifie le test 2 (dongle initialisé). Sur le téléphone, oublie l'ancien appareil <code>AutoKit-xxxx</code> s'il existe, puis recherche à nouveau. Le nom peut rester <code>AutoKit-xxxx</code> selon le firmware.</td></tr>
<tr><td>Bluetooth associé, mais <b>Android Auto ne démarre jamais</b></td><td>1) Android 11 ou plus ? Wi-Fi 5 GHz ? Android Auto à jour ? 2) Sur le téléphone : <i>Paramètres Android Auto → Android Auto sans fil</i> activé. 3) Diagnostic › <i>Téléphone vu par le dongle</i> : si « aucun », le dongle ne propose pas Android Auto → firmware trop ancien (voir ci-dessous).</td></tr>
<tr><td>Firmware sans Android Auto</td><td>Dernier recours : mise à jour du firmware du dongle selon la procédure Carlinkit. <b>Note d'abord le firmware actuel</b> et sache qu'il faudra revérifier FK2Play ensuite. Demande conseil sur le fil XDA avant.</td></tr>
<tr><td>Écran noir au retour sur FK2Droid</td><td>Attends 6 secondes : FK2Droid rouvre la connexion tout seul (message « Image perdue : reconnexion… »). Photographie Diagnostic › <i>Images clés</i>.</td></tr>
<tr><td>Image qui saccade</td><td>20 images/s, puis résolution plus basse. Vérifie Diagnostic › <i>Décodeur vidéo actif</i> (attendu : Matériel OMX.Nvidia…).</td></tr>
<tr><td>Coupures du sans-fil</td><td>Téléphone à moins d'un mètre du dongle, coque métallique retirée. Évite les points d'accès Wi-Fi 5 GHz du téléphone pendant la conduite.</td></tr>
<tr><td>Le tactile est décalé ou ne répond plus</td><td>Décoche <i>Tactile multipoint</i>.</td></tr>
<tr><td>Le mode nuit ne suit pas les phares</td><td>Diagnostic › <i>État du Honda</i> : si « service absent » ou « erreur », règle le mode nuit sur Toujours jour / Toujours nuit et signale la ligne.</td></tr>
<tr><td>Pas de son</td><td>Process Controls : SoundOut ON. Sinon décoche « Son via l'autoradio (USB) ».</td></tr>
<tr><td>Volume du volant sans effet</td><td>Process Controls : SoundInterrupt et SoundInterruptMute sur <b>OFF</b>.</td></tr>
<tr><td>Appel : pas de son, ou on ne t'entend pas</td><td>Coche <i>Appels via le Bluetooth de la voiture</i> et garde le téléphone connecté à HandsFreeLink. Sinon : dongle CCPA-MIC.</td></tr>
<tr><td>L'Assistant Google ne t'entend pas</td><td>Le micro de la voiture n'est pas accessible aux applis : seul un dongle CCPA-MIC permet de lui parler.</td></tr>
<tr><td>FK2Play s'ouvre à la place de FK2Droid</td><td>Réglages → Applications → FK2Play → Effacer les valeurs par défaut.</td></tr>
<tr><td>FK2Droid se ferme en roulant</td><td>Process Controls : ProcessKillTarget OFF, LastMode ON.</td></tr>
</table>
"""

def interdits():
    return """
<ul>
<li><b>Aucune mise à jour du Honda Connect</b> chez le concessionnaire : elle se termine par une remise à zéro qui
efface les applis, et à partir de la RC7 l'installation d'applis est bloquée.</li>
<li>Ne supprime jamais la ligne <code>HondaAppCenter_A1.apk</code> dans Allowed Installations.</li>
<li>Pas de hub USB, pas de rallonge douteuse : le dongle consomme jusqu'à 5 V / 1 A.</li>
<li>Ne coupe pas le contact pendant une installation. N'utilise pas l'écran en roulant.</li>
</ul>
<h3>Revenir en arrière</h3>
<ul>
<li>Débrancher le dongle suffit à arrêter Android Auto : FK2Droid ne modifie rien dans le système.</li>
<li>Pour supprimer l'appli : <b class="menu">Réglages → Applications → FK2Droid → Désinstaller</b>. FK2Play n'est pas touché.</li>
<li>La ligne <code>com.fk2droid</code> de Process Controls peut être supprimée dans Honda Permissions.</li>
</ul>
"""

def fiche():
    rows = [
        ("Numéro de build du Honda Connect / version RC", ""),
        ("Téléphone (marque, modèle, version d'Android)", ""),
        ("FK2Play aussi installé", "☐ oui  ☐ non"),
        ("Ligne de diagnostic sans dongle", ""),
        ("Message « Firmware dongle : … »", ""),
        ("Fenêtre d'autorisation USB apparue", "☐ oui  ☐ non"),
        ("Nom Bluetooth vu sur le téléphone", "☐ FK2Droid  ☐ AutoKit-…  ☐ rien"),
        ("Android Auto affiché", "☐ oui  ☐ non — délai :"),
        ("Message de connexion exact", ""),
        ("Fluidité de l'image", "☐ fluide  ☐ saccades  ☐ inutilisable"),
        ("Tactile précis (et multipoint si essayé)", "☐ oui  ☐ décalé  ☐ ne répond pas"),
        ("Musique / voix du GPS", "☐ OK  ☐ pas de son  ☐ haché"),
        ("Retour sur Android Auto depuis la radio", "☐ immédiat  ☐ après relance  ☐ écran noir"),
        ("Appel téléphonique", "☐ OK  ☐ je n'entends pas  ☐ on ne m'entend pas"),
        ("Touches du volant (piste, volume)", "☐ OK  ☐ non"),
        ("Mode nuit suit les phares", "☐ oui  ☐ non"),
        ("Retour auto après caméra de recul", "☐ oui  ☐ non"),
        ("Diagnostic › Images clés", ""),
        ("Diagnostic › État du Honda", ""),
        ("Diagnostic › Décodeur vidéo actif", ""),
        ("Remarques / messages d'erreur exacts", "<br><br>"),
    ]
    t = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    return f"""<p>À joindre à ton retour (une photo suffit) : issue GitHub ou fil XDA « Honda Connect Android System ».</p>
<table class="check"><tr><th>Point</th><th>Résultat</th></tr>{t}</table>
<p class="small">FK2Droid {VER} · minSdk 15 (Android 4.0.4) · paquet <code>com.fk2droid</code> · dongles reconnus :
USB 1314:1520 et 1314:1521 · signé avec la clé FK2Play (SHA-256 8D:F7:C2:BD…D6:CC:29:26). Honda Permissions est un
outil communautaire non officiel : son auteur et moi ne pouvons garantir l'absence de risque pour l'autoradio.
Android Auto est une marque de Google LLC. Non affilié à Google, Honda ni Carlinkit.</p><p class="small" style="">Remerciements : MaKi83 (OpenDroidAuto) pour le décodeur vidéo matériel, le service volant et la
lecture jour / nuit et caméra du Honda ; S_Mike pour Honda Permissions ; la communauté node-carplay / pycarplay pour la
documentation du protocole du dongle ; les membres du fil XDA « Honda Connect Android System ».</p>"""

SECURITE = """<div class="box stop"><b>Sécurité.</b> Tout se fait à l'arrêt, frein à main serré, moteur tournant (la batterie
ne doit pas faiblir pendant une installation). Ne coupe jamais le contact pendant une installation. N'utilise pas l'écran
en roulant. Compte environ 30 minutes (10 minutes si FK2Play est déjà installé).</div>"""

# ---------------------------------------------------------------- les deux guides

def guide_rc3():
    b = nouveautes()
    b += f"""<div class="pb"></div>
<h1>Installer Android Auto sur un Honda Connect RC3</h1>
<div class="sub">Civic FK2 / Type R, HR-V, CR-V, Jazz… · Android 4.0.4 · build <code>09.08C.00.xxxx</code> (RC3) ·
dongle Carlinkit CPC200-CCPA · FK2Droid {VER} · {DATE}</div>
<div class="box info">Ce guide est réservé à la <b>RC3</b> (build <code>09.08C.00.xxxx</code>, par exemple
<code>09.08C.00.1123</code> avec le logiciel principal <code>31.00.cf</code>). Pour une autre version, utilise le mode
d'emploi « toutes versions ».</div>
{SECURITE}
<h3>Sommaire</h3>
<div class="toc"><ol>
<li>Comment ça marche</li><li>Ce qu'il te faut</li><li>Vérifier que tu es en RC3</li><li>Installer Honda Permissions</li>
<li>Installer FK2Droid</li><li>Donner les droits à FK2Droid</li><li>FK2Play et FK2Droid ensemble</li>
<li>Test 1 : sans le dongle</li><li>Test 2 : brancher le dongle</li><li>Test 3 : connecter le téléphone Android</li>
<li>Réglages de FK2Droid</li><li>Dépannage</li><li>Ce qu'il ne faut pas faire · revenir en arrière</li><li>Fiche de résultats</li>
</ol></div>
<div class="box ok"><b>Chemin rapide si FK2Play marche déjà sur ta voiture :</b> étapes 5, 6, 7, puis 9 et 10
(Honda Permissions, le dongle et HandsFreeLink sont déjà prêts).</div>
<h2>1. Comment ça marche</h2>{schema()}
<h2>2. Ce qu'il te faut</h2>{besoin(True)}
<h2>3. Vérifier que tu es en RC3</h2>{lire_build(True)}
<h2>4. Installer Honda Permissions</h2>{honda_perms(True)}
<h2>5. Installer FK2Droid</h2>{installer(True)}
<h2>6. Donner les droits à FK2Droid</h2>{droits()}
<h2>7. FK2Play et FK2Droid ensemble</h2>{cohabitation()}
<h2>8. Test 1 : sans le dongle</h2>{test1()}
<h2>9. Test 2 : brancher le dongle</h2>{test2()}
<h2>10. Test 3 : connecter le téléphone Android</h2>{test3(True)}
<h2>11. Réglages de FK2Droid</h2>{reglages()}
<h2>12. Dépannage</h2>{depannage()}
<h2>13. Ce qu'il ne faut pas faire</h2>{interdits()}
<div class="pb"></div><h2>14. Fiche de résultats</h2>{fiche()}
"""
    return html("Mode d'emploi RC3", b)

def guide_tous():
    b = nouveautes()
    b += f"""<div class="pb"></div>
<h1>FK2Droid — mode d'emploi toutes versions</h1>
<div class="sub">Android Auto sur le Honda Connect gen 1 (Android 4.0.4) avec un dongle Carlinkit CPC200-CCPA ·
RC3 à RC8 · FK2Droid {VER} · {DATE}</div>
{SECURITE}
<div class="box ok"><b>Si FK2Play marche déjà sur ta voiture :</b> Honda Permissions est en place, quelle que soit ta
RC. Va directement aux étapes 4, 5 et 6, puis 7 à 9.</div>
<h2>1. Comment ça marche et ce qu'il te faut</h2>{schema()}{besoin(False)}
<h2>2. Noter la version (build) du Honda Connect</h2>{lire_build(False)}
<h2>3. Installer Honda Permissions (une seule fois)</h2>{honda_perms(False)}
<h2>4. Installer FK2Droid</h2>{installer(False)}
<h2>5. Régler FK2Droid dans Honda Permissions</h2>{droits()}
<h2>6. FK2Play et FK2Droid ensemble</h2>{cohabitation()}
<h2>7. Test 1 — sans le dongle</h2>{test1()}
<h2>8. Test 2 — brancher le dongle</h2>{test2()}
<h2>9. Test 3 — connecter le téléphone Android</h2>{test3(False)}
<h2>10. Réglages</h2>{reglages()}
<h2>11. Dépannage</h2>{depannage()}
<h2>12. Ce qu'il ne faut pas faire · revenir en arrière</h2>{interdits()}
<div class="pb"></div><h2>Fiche de résultats</h2>{fiche()}
"""
    return html("Mode d'emploi toutes versions", b)

if __name__ == "__main__":
    for name, fn in (("Mode_emploi_FK2Droid_RC3", guide_rc3), ("Mode_emploi_FK2Droid_toutes_versions", guide_tous)):
        with open(os.path.join(HERE, name + ".html"), "w", encoding="utf-8") as f:
            f.write(fn())
    print("HTML ok")
