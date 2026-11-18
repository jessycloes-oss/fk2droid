#!/usr/bin/env python3
"""English user guides for FK2Droid (RC3 illustrated + all versions): HTML, then PDF with headless Chrome."""
import os
from gen import CSS, step, VER, HERE

DATE = "18 November 2026"


def html(title, body):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>{CSS}</style></head><body>{body}</body></html>"""


def img_if(name, caption, h=52):
    if not os.path.exists(os.path.join(HERE, "img", name)):
        return ""
    return f"""<figure style="margin:2mm 0 3mm 0"><img src="img/{name}" style="max-height:{h}mm">
<figcaption>{caption}</figcaption></figure>"""


def news():
    return f"""
<h1>FK2Droid {VER} — read me first</h1>
<div class="sub">Android Auto on the Honda Connect · first test version · {DATE}</div>

<div class="box warn"><b>Test version, not yet road-tested.</b> FK2Droid reuses the whole engine of <b>FK2Play 2.1</b>
(road-tested: picture decoded by the Tegra 3, touch, sound, calls through the stock hands-free kit, steering wheel
buttons, background mode). The Android Auto part was checked on a simulated Honda Connect (Android 4.0.4), not yet in a
car: your feedback will decide what goes into 1.0.</div>

<p><b>In one sentence:</b> it is FK2Play for <b>Android</b> phones: the same Carlinkit CPC200-CCPA dongle is switched to
<b>Android Auto</b> mode, and FK2Droid shows Android Auto on the Honda Connect's 7" screen, just like FK2Play shows CarPlay.</p>

<h3>What is new compared with FK2Play</h3>
<table style="font-size:8.4pt">
<tr><th style="width:32%">Feature</th><th>Details</th></tr>
<tr><td>Dongle Android Auto mode</td><td>FK2Droid sends <code>android_work_mode = 1</code> to the dongle at every connection and
again after each phone disconnection (the dongle forgets it).</td></tr>
<tr><td>Automatic night mode</td><td>Follows the Honda lighting (headlights on → dark Google Maps). Read from the Honda
Connect state service, a method discovered by MaKi83 (OpenDroidAuto).</td></tr>
<tr><td>Return after the reverse camera</td><td>If Android Auto was on screen when you engaged reverse, FK2Droid comes back to
it by itself when the camera turns off.</td></tr>
<tr><td>Display size</td><td>Density sent to the phone (bigger or smaller buttons).</td></tr>
<tr><td>Multi-touch (option)</td><td>Pinch to zoom in Google Maps. Off by default: worth a try.</td></tr>
<tr><td>Picture not coming back</td><td>If the phone sends no picture when you return to FK2Droid, the connection is reopened
automatically (2 times at most). A diagnostic line shows whether it happened.</td></tr>
<tr><td>Bluetooth name · language</td><td>The dongle shows up as <b>FK2Droid</b> (can be changed). The app is in English, or in
French when the Honda Connect is set to French (since 1.0-test2).</td></tr>
</table>

<h3>Test in the car, in this order</h3>
<ol style="font-size:9.1pt">
<li>The Android phone connects and Android Auto shows up (message <span class="ui">Android Auto connected (wireless)</span>).</li>
<li>Touch, music, navigation voice, steering wheel track buttons.</li>
<li>Leave FK2Droid (radio, settings) then come back: the picture should return within 2 seconds.</li>
<li>A phone call (with the option "Calls via the car's Bluetooth").</li>
<li>Switch the headlights on: the map turns dark within a few seconds.</li>
<li>Reverse gear from the Android Auto screen, then drive: automatic return to Android Auto.</li>
</ol>
<p>Then take a photo of <b class="menu">FK2Droid settings › Diagnostics</b>: lines <i>Phone seen by the dongle</i>,
<i>Key frames</i>, <i>Honda state</i> and <i>Active video decoder</i>.</p>

<div class="box info" style="font-size:8.9pt"><b>Already using FK2Play?</b> FK2Droid installs <b>next to it</b> (separate app,
package <code>com.fk2droid</code>), with the same dongle and the same signing key. Honda Permissions is already in place:
go straight to "Install FK2Droid". Only one of the two apps can use the dongle at a time (see "FK2Play and FK2Droid
together").</div>
"""


def diagram():
    return """
<div class="diagram">
  <div class="node"><b>Android phone</b>Android 11 or later<br>Android Auto app</div>
  <div class="arrow">Bluetooth + 5 GHz Wi-Fi<br>⇢ ⇢ ⇢<br>(wireless)</div>
  <div class="node"><b>Carlinkit CPC200-CCPA dongle</b>the same as for FK2Play<br>in Android Auto mode</div>
  <div class="arrow">USB cable<br>picture, sound ⇢<br>⇠ touch, buttons</div>
  <div class="node"><b>Honda Connect</b>Android 4.0.4<br>FK2Droid shows Android Auto</div>
</div>
<p>The Honda Connect is too old to run Android Auto itself. The dongle handles everything on the Google side: FK2Droid
receives the picture (H.264 video), decodes it with the Tegra 3 video chip, plays the sound and sends back touch and
buttons.</p>
"""


def needs():
    return f"""
<table>
<tr><th style="width:30%">Item</th><th>Details</th></tr>
<tr><td>Carlinkit CPC200-CCPA dongle</td><td>The "Autokit" model for Android head units, <b>the same as for FK2Play</b>
(USB <code>1314:1520</code> or <code>1314:1521</code>). Not a 5.0 / 2Air / U2W / Mini. The CCPA-MIC version (built-in
microphone) is recommended if you want to talk to Google Assistant (the car microphone is not reachable by apps).</td></tr>
<tr><td>Android phone</td><td><b>Android 11 or later</b>, <b>5 GHz</b> Wi-Fi, up-to-date <b>Android Auto</b> app (Play Store),
mobile data on. Google requires Android 11 and 5 GHz Wi-Fi for wireless Android Auto.</td></tr>
<tr><td>FK2Droid</td><td><code>HondaAppCenter_A1.apk</code> (FK2Droid already renamed, ready to copy) or
<code>FK2Droid-{VER}.apk</code>, from the GitHub release.</td></tr>
<tr><td>USB stick</td><td>FAT32, 32 GB max, preferably empty.</td></tr>
<tr><td>Honda Permissions (S_Mike)</td><td>Already installed if you use FK2Play. Otherwise: XDA forum, thread "Honda Connect
Android System", or cmdroid.com (not provided here, another author's tool).</td></tr>
<tr><td>This guide</td><td>Printed or on a tablet, with the results sheet (last page).</td></tr>
</table>
<div class="box warn"><b>Dongle firmware.</b> According to sellers, the CPC200-CCPA does wireless Android Auto with recent
firmwares, and only CarPlay (or wired Android Auto) with some older ones. <b>Start without updating anything</b>: FK2Droid
shows <span class="ui">Dongle firmware: …</span> when you plug it in; note it on the results sheet. Only consider a firmware
update if Android Auto never shows up (see Troubleshooting), as it may change how the dongle behaves with FK2Play.</div>
"""


VERSIONS = """
<table>
<tr><th>Build number shown</th><th>Version</th><th>Android</th><th>Installing Honda Permissions</th><th>FK2Droid</th></tr>
<tr><td><code>09.08C.00.xxxx</code><br><span class="small">e.g. 09.08C.00.1123, 09.08C.00.0021</span></td><td><b>RC3</b></td><td>4.0.4</td><td>Easy: renaming trick (step 3A) — RC3 illustrated guide</td><td>✔ main target</td></tr>
<tr><td><code>0C.091.xx.xxxx</code></td><td><b>RC5</b></td><td>4.0.4</td><td>Easy (step 3A)</td><td>✔ expected, to be confirmed</td></tr>
<tr><td><code>0E.094.00.xxxx</code></td><td><b>RC6 / RC6.1</b></td><td>4.0.4</td><td>Easy (step 3A)</td><td>✔ expected, to be confirmed</td></tr>
<tr><td><code>0F.095.01.xxxx</code></td><td><b>RC7</b></td><td>4.0.4</td><td>Hard: back to RC6 or iRoot (step 3B)</td><td>✔ once Honda Permissions is in place</td></tr>
<tr><td><code>10.096.00.xxxx</code> (or 10.96…)</td><td><b>RC8</b></td><td>4.0.4</td><td>Hard (step 3B)</td><td>✔ once Honda Permissions is in place</td></tr>
</table>
<p class="small">Numbers collected on the XDA forum ("Honda Connect Android System" thread) and checked for RC3 on the
developer's Civic Type R FK2. FK2Droid does not depend on the RC: only installing Honda Permissions and the install lock
change between versions. The steering wheel service and the Honda day/night state were checked on RC3; on other RCs, if
they do not answer, FK2Droid still works (the diagnostic lines will tell).</p>
"""


def read_build(rc3):
    t = """<div class="cols"><div><ol>
<li>On the head unit: <b class="menu">HOME → Settings → Android → About device</b>.</li>
<li>Read the <b>Build number</b> line and write it on the results sheet.</li>
<li>Find your version in the table below: it tells you which path to follow.</li></ol></div>"""
    if rc3:
        t += """<div><figure><img src="img/exemple-version-rc3.jpg" style="max-height:52mm">
<figcaption>A real RC3 Honda Connect: build 09.08C.00.1123, Android 4.0.4, kernel 3.1.10.</figcaption></figure></div>"""
    return t + "</div>" + VERSIONS


def honda_perms(rc3):
    a = """
<h3>3A. Versions RC3 to RC6.1 (renaming trick)</h3>
<ol>
<li>On the PC, rename the Honda Permissions file to <code>HondaAppCenter_A1.apk</code> and copy it alone to the root of the
USB stick. On Windows, enable <i>View → File name extensions</i> to avoid <code>HondaAppCenter_A1.apk.apk</code>.</li>
<li>In the car, plug in the stick, open the APK installer (<i>Install apk</i>), pick the file and tap <b>Install</b>.</li>
<li>If the install is refused: Android factory reset (<b class="menu">HOME → Settings → Android → Backup &amp; reset</b>),
refuse any Honda app update, then try again. This erases paired phones and added apps.</li>
<li>Open Honda Permissions → <b>Allowed Installations</b>. Long press <code>HondaAppCenter_A1.apk</code> → pencil →
<b>Sig digest sha256</b> = <code>PREINSTALL</code> → save. <b>Never delete this line.</b></li>
<li>Back up Honda Permissions to the stick (backup function).</li>
</ol>"""
    b = """
<h3>3B. Versions RC7 and RC8</h3>
<div class="box stop">The renaming trick is blocked from RC7 on. Two ways exist on XDA, both riskier: <b>go back to RC6</b>
with the files shared on the forum then do step 3A, or <b>iRoot</b> to inject Honda Permissions. Going back from RC6 to RC8
caused a boot loop for one user: read the XDA thread carefully before touching the firmware, and ask for help if in doubt.</div>"""
    if rc3:
        return ("""<div class="box ok"><b>You are on RC3:</b> the easiest case, no firmware change and no root needed.
<b>If Honda Permissions is already installed (you use FK2Play), skip this step.</b></div>""" + a)
    return ("""<div class="box ok">If the Honda Permissions icon is already there (for instance because FK2Play is installed),
go straight to step 4.</div>""" + a + b)


def install():
    return f"""
<ol>
<li>On the PC, empty the stick, then copy <code>HondaAppCenter_A1.apk</code> from the release to its root. <b>It really is
FK2Droid</b> (same file name as for FK2Play: it is the name the Honda accepts).</li>
<li>In the car, plug in the stick → APK installer → <code>HondaAppCenter_A1.apk</code> → <b>Install</b>.</li>
<li>Remove the stick. Two icons appear: <b>FK2Droid</b> (green "FK2 droid" square) and <b>FK2Droid settings</b>.
FK2Play, if installed, stays and is not changed.</li>
</ol>
<div class="box info"><b>Install button greyed out?</b> In Honda Permissions → Allowed Installations, tap +, then
<i>APK Name</i> <code>application.apk</code>, <i>Package name</i> empty, <i>Sig digest</i> <code>PREINSTALL</code>. Then copy
<code>FK2Droid-{VER}.apk</code> renamed to <code>application.apk</code>.</div>
<p class="small">Later updates: same method with the new <code>HondaAppCenter_A1.apk</code>. FK2Droid updates and keeps its
settings. Always close FK2Droid first (unplug the dongle).</p>
"""


PROCESS = """
<table>
<tr><th style="width:42%">Field</th><th>Value</th></tr>
<tr><td>Process name</td><td><code>com.fk2droid</code></td></tr>
<tr><td>Package name</td><td><code>com.fk2droid</code></td></tr>
<tr><td>Auth Type</td><td>THIRD_PARTY</td></tr>
<tr><td>App Type</td><td>NAVI (Android Auto is mostly used for navigation)</td></tr>
<tr><td>SoundOut · LastMode</td><td>☑ ON</td></tr>
<tr><td>SoundInterrupt · SoundInterruptMute</td><td>☐ <b>OFF</b> (otherwise the steering wheel volume stops working)</td></tr>
<tr><td>VideoOut · OomSetPerm</td><td>☐ OFF</td></tr>
<tr><td>ProcessKillTarget</td><td>☐ OFF (stops the Honda from closing FK2Droid)</td></tr>
</table>
"""


def rights():
    return f"""
<p>Without this step, the Honda Connect may mute FK2Droid or close it while driving.</p>
<ol>
<li>Open Honda Permissions → <b>Process Controls</b> → <b>+</b>.</li>
<li>Fill in as below (same values as the <code>com.fk2play</code> line validated on 15 November 2026, only the name changes).</li>
<li>Save, then make another backup to the stick.</li>
</ol>
{PROCESS}
"""


def together():
    return """
<p>FK2Play (iPhone, CarPlay) and FK2Droid (Android, Android Auto) can both stay installed, but <b>only one can use the
dongle at a time</b>.</p>
<ul>
<li><b>When the dongle is plugged in</b>, Android asks which app to open. If you ticked <i>Use by default</i> for FK2Play,
it opens by itself: to be able to choose, go to <b class="menu">Settings → Applications → FK2Play → Clear defaults</b>.</li>
<li><b>One driver, one phone</b>: tick <i>Use by default</i> for the right app.</li>
<li><b>iPhone and Android in the household</b>: do not tick <i>Use by default</i>; the question shows at every start and you choose.</li>
<li><b>Switching apps</b>: unplug the dongle for 5 seconds, plug it back and pick the other app. Do not start one while the
other is already showing its screen.</li>
</ul>
<div class="box info">FK2Droid is not meant for iPhones, but it does recognise CarPlay (message
<span class="ui">CarPlay connected (iPhone)</span>). For an iPhone, keep FK2Play, which is road-tested.</div>
"""


def test1():
    return """
<ol>
<li>Start <b>FK2Droid</b>. The screen turns black with a message in the middle.</li>
<li>Write down the line in brackets, for example <span class="ui">[Android USB host: yes | no device seen]</span>.</li>
</ol>
<table><tr><th>Line shown</th><th>Meaning</th></tr>
<tr><td><span class="ui">Android USB host: yes</span></td><td>Good sign: go on.</td></tr>
<tr><td><span class="ui">Android USB host: NO</span></td><td>Go on anyway: test 2 decides.</td></tr></table>
"""


def test2():
    return """
<ol>
<li>With FK2Droid open, plug the dongle <b>directly</b> into the console USB port (no hub).</li>
<li>If Android asks "Allow FK2Droid to access the USB device?", tap <b>OK</b> (see "FK2Play and FK2Droid together" for the
<i>Use by default</i> box).</li>
<li>Wait 5 to 10 seconds and write down what shows up:</li>
</ol>
<table><tr><th style="width:45%">Message</th><th>Meaning and next step</th></tr>
<tr><td><span class="ui">Dongle ready, waiting for the Android phone...</span> and/or <span class="ui">Dongle firmware: 20xx...</span></td>
<td>✔ The head unit drives the dongle and switched it to Android Auto mode. Note the firmware, go to test 3.</td></tr>
<tr><td><span class="ui">Plug the Carlinkit dongle...</span> with <span class="ui">seen: 1314:1520</span> or <span class="ui">1314:1521</span></td>
<td>Dongle seen but not opened. Check that FK2Play is not running (unplug / replug), restart FK2Droid once.</td></tr>
<tr><td><span class="ui">seen: xxxx:yyyy</span> (another number)</td><td>Another dongle model: please report this number.</td></tr>
<tr><td><span class="ui">Allow access to the USB dongle</span> stays on screen</td><td>Unplug the dongle, plug it back, accept the window.</td></tr>
<tr><td><span class="ui">Error: ... - retrying...</span> in a loop</td><td>Write down the exact error text.</td></tr>
</table>
"""


def test3():
    return f"""
<h3>Prepare the phone (once)</h3>
<ol>
<li>Update <b>Android Auto</b> (Play Store) and Google Play services. Turn Wi-Fi, Bluetooth and mobile data on.</li>
<li><b>Calls</b> (the car microphone is not reachable by apps): keep the phone connected to <b>HandsFreeLink</b>, the Honda's
stock Bluetooth, and tick <b class="menu">FK2Droid settings → Audio → Calls via the car's Bluetooth</b>. Music stays on USB;
the Honda takes every call with its own microphone and the steering wheel buttons, then FK2Droid returns to Android Auto.</li>
</ol>
<h3>First connection</h3>
{step(1, "On the phone: <b>Settings → Connected devices → Pair new device</b>, choose <b>FK2Droid</b> (or <code>AutoKit-xxxx</code> depending on the dongle firmware). Accept the pairing code.")}
{step(2, "The phone offers Android Auto: accept every request (permissions, \"Use Android Auto with this vehicle?\"). <b>Unlock the phone</b> the first time.")}
{step(3, "The dongle moves the phone to 5 GHz Wi-Fi by itself. After 10 to 40 seconds, Android Auto shows on the Honda and FK2Droid briefly says <span class='ui'>Android Auto connected (wireless)</span>.")}
{step(4, "Try and tick on the sheet: touch, music, navigation voice, a call, steering wheel buttons, night mode, reverse camera.")}
{img_if("fk2droid-connecte.png", "Real capture of FK2Droid on a simulated Honda Connect (Android 4.0.4) with a fake dongle in Android Auto mode: a test pattern replaces the Android Auto screen.", 48)}
<p>Next times, the connection is automatic when the car starts, phone in your pocket.</p>
<table><tr><th style="width:45%">What you see</th><th>What it means</th></tr>
<tr><td><span class="ui">Android Auto connected (wireless)</span></td><td>✔ All good.</td></tr>
<tr><td><span class="ui">Android Auto connected (wired)</span></td><td>✔ The dongle does Android Auto over a cable (depends on firmware).</td></tr>
<tr><td><span class="ui">CarPlay connected (iPhone)</span></td><td>An iPhone connected: use FK2Play.</td></tr>
<tr><td><span class="ui">Android screen mirroring connected</span></td><td>The dongle did not switch to Android Auto: unplug / replug it; if it persists, see Troubleshooting (firmware).</td></tr>
<tr><td>The phone does not show up / never offers Android Auto</td><td>See Troubleshooting.</td></tr>
</table>
"""


def settings():
    pics = ""
    a = img_if("fk2droid-reglages-en.png", "Real FK2Droid settings screen (simulated Android 4.0.4, English).", 56)
    b = img_if("fk2droid-diagnostic-en.png", "FK2Droid's own diagnostic lines after a simulated connection and a return from the home screen.", 56)
    if a or b:
        pics = f'<div class="cols"><div>{a}</div><div>{b}</div></div>'
    return f"""
<p><b>FK2Droid settings</b> icon in the app list, the head unit's MENU key, or a long press on the status message.
Settings that concern the dongle apply when you return to FK2Droid (reconnection of a few seconds).</p>
{pics}
<table>
<tr><th style="width:38%">Setting</th><th style="width:16%">Default</th><th>What it does</th></tr>
<tr><td>Video › Resolution / Frames per second</td><td>800x480 · 30</td><td>Lower them if the picture stutters.</td></tr>
<tr><td>Video › Video decoder</td><td>Automatic</td><td>Tegra 3 video chip, falls back to software. "Software only" as a fallback.</td></tr>
<tr><td>Video › <b>Android Auto night mode</b></td><td>Automatic</td><td>Follows the Honda lighting. "Always day" / "Always night" if you prefer.</td></tr>
<tr><td>Video › <b>Android Auto display size</b></td><td>160</td><td>Density sent to the phone: 120 = more information, 200 = bigger buttons.</td></tr>
<tr><td>Video › <b>Multi-touch</b></td><td>off</td><td>Pinch to zoom in Maps. Untick if touch misbehaves.</td></tr>
<tr><td>Audio › Steering wheel music buttons</td><td>on</td><td>Next / previous track from the wheel while Android Auto is shown.</td></tr>
<tr><td>Audio › Calls via the car's Bluetooth</td><td>off</td><td><b>Tick it</b> on the Honda Connect (see test 3).</td></tr>
<tr><td>Audio › <b>Return to Android Auto after the reverse camera</b></td><td>on</td><td>Automatic return after reversing.</td></tr>
<tr><td>Audio › Return to Android Auto as soon as a call ends</td><td>on</td><td>Without waiting for the Honda to leave its phone screen.</td></tr>
<tr><td>Audio › Android Auto sound through the head unit (USB)</td><td>on</td><td>Untick to send the sound over Bluetooth.</td></tr>
<tr><td>Connection › <b>Dongle Bluetooth name</b></td><td>FK2Droid</td><td>Name shown on the phone (16 characters max).</td></tr>
<tr><td>Connection › 5 GHz Wi-Fi</td><td>on</td><td>Keep it: wireless Android Auto requires 5 GHz.</td></tr>
<tr><td>Diagnostics › <b>Phone seen by the dongle</b></td><td>—</td><td>Connection type received (Android Auto, CarPlay, mirroring) and time.</td></tr>
<tr><td>Diagnostics › <b>Key frames</b></td><td>—</td><td>"OK: key frame received in … ms" or "NO ANSWER": tells whether returning to Android Auto is instant.</td></tr>
<tr><td>Diagnostics › <b>Restart if the picture does not come back</b></td><td>on</td><td>Reopens the connection if the screen stays black on return.</td></tr>
<tr><td>Diagnostics › <b>Honda state</b></td><td>—</td><td>"day / night, Honda screen N": checks the headlights and camera reading.</td></tr>
<tr><td>Diagnostics › Active video decoder · Honda steering wheel service · Last keys received</td><td>—</td><td>As in FK2Play 2.1.</td></tr>
</table>
<h3>Steering wheel buttons (as in FK2Play 2.0)</h3>
<table><tr><th>Button</th><th>On the Android Auto screen</th><th>Elsewhere</th></tr>
<tr><td>Next / previous track</td><td>Next / previous song</td><td>Usual Honda function</td></tr>
<tr><td>Volume + / −</td><td>Honda volume (shown on the dashboard)</td><td>Same</td></tr>
<tr><td>Hang up (during a call)</td><td>Hangs up</td><td>Stock hands-free kit</td></tr></table>
<p><b>Android Auto keeps running in the background</b>: you can go to the radio or the settings, music, voice guidance and
the connection go on. To come back, tap the FK2Droid icon or its notification.</p>
"""


def trouble():
    return """
<table>
<tr><th style="width:34%">Problem</th><th>What to try</th></tr>
<tr><td>The phone does not see <b>FK2Droid</b> over Bluetooth</td><td>Check test 2 (dongle ready). On the phone, forget any old <code>AutoKit-xxxx</code> device, then search again. The name may stay <code>AutoKit-xxxx</code> depending on the firmware.</td></tr>
<tr><td>Bluetooth paired, but <b>Android Auto never starts</b></td><td>1) Android 11 or later? 5 GHz Wi-Fi? Android Auto up to date? 2) On the phone: <i>Android Auto settings → Wireless Android Auto</i> on. 3) Diagnostics › <i>Phone seen by the dongle</i>: if "none", the dongle does not offer Android Auto → firmware too old (see below).</td></tr>
<tr><td>Firmware without Android Auto</td><td>Last resort: update the dongle firmware following Carlinkit's procedure. <b>Note the current firmware first</b>, and FK2Play will need checking again afterwards. Ask on the XDA thread before.</td></tr>
<tr><td>Black screen when returning to FK2Droid</td><td>Wait 6 seconds: FK2Droid reopens the connection by itself (message "Picture lost: reconnecting…"). Take a photo of Diagnostics › <i>Key frames</i>.</td></tr>
<tr><td>Stuttering picture</td><td>20 fps, then a lower resolution. Check Diagnostics › <i>Active video decoder</i> (expected: Hardware OMX.Nvidia…).</td></tr>
<tr><td>Wireless drops</td><td>Phone less than a metre from the dongle, metal case removed. Avoid using the phone's 5 GHz hotspot while driving.</td></tr>
<tr><td>Touch offset or not responding</td><td>Untick <i>Multi-touch</i>.</td></tr>
<tr><td>Night mode does not follow the headlights</td><td>Diagnostics › <i>Honda state</i>: if "service missing" or "error", set night mode to Always day / Always night and report the line.</td></tr>
<tr><td>No sound</td><td>Process Controls: SoundOut ON. Otherwise untick "Android Auto sound through the head unit (USB)".</td></tr>
<tr><td>Steering wheel volume does nothing</td><td>Process Controls: SoundInterrupt and SoundInterruptMute <b>OFF</b>.</td></tr>
<tr><td>Call: no sound, or they cannot hear you</td><td>Tick <i>Calls via the car's Bluetooth</i> and keep the phone connected to HandsFreeLink. Otherwise: CCPA-MIC dongle.</td></tr>
<tr><td>Google Assistant cannot hear you</td><td>The car microphone is not reachable by apps: only a CCPA-MIC dongle lets you talk to it.</td></tr>
<tr><td>FK2Play opens instead of FK2Droid</td><td>Settings → Applications → FK2Play → Clear defaults.</td></tr>
<tr><td>FK2Droid closes while driving</td><td>Process Controls: ProcessKillTarget OFF, LastMode ON.</td></tr>
</table>
"""


def donts():
    return """
<ul>
<li><b>No Honda Connect update</b> at the dealer: it ends with a reset that erases the apps, and from RC7 on installing apps is blocked.</li>
<li>Never delete the <code>HondaAppCenter_A1.apk</code> line in Allowed Installations.</li>
<li>No USB hub, no dubious extension cable: the dongle draws up to 5 V / 1 A.</li>
<li>Do not switch the ignition off during an install. Do not use the screen while driving.</li>
</ul>
<h3>Going back</h3>
<ul>
<li>Unplugging the dongle is enough to stop Android Auto: FK2Droid changes nothing in the system.</li>
<li>To remove the app: <b class="menu">Settings → Applications → FK2Droid → Uninstall</b>. FK2Play is not touched.</li>
<li>The <code>com.fk2droid</code> line in Process Controls can be deleted in Honda Permissions.</li>
</ul>
"""


def sheet():
    rows = [
        ("Honda Connect build number / RC version", ""),
        ("Phone (brand, model, Android version, Android Auto version)", ""),
        ("FK2Play also installed", "☐ yes  ☐ no"),
        ("Diagnostic line without the dongle", ""),
        ("\"Dongle firmware: …\" message", ""),
        ("USB permission window shown", "☐ yes  ☐ no"),
        ("Bluetooth name seen on the phone", "☐ FK2Droid  ☐ AutoKit-…  ☐ nothing"),
        ("Android Auto shown", "☐ yes  ☐ no — delay:"),
        ("Exact connection message", ""),
        ("Picture smoothness", "☐ smooth  ☐ stutters  ☐ unusable"),
        ("Touch accurate (and multi-touch if tried)", "☐ yes  ☐ offset  ☐ not responding"),
        ("Music / navigation voice", "☐ OK  ☐ no sound  ☐ choppy"),
        ("Return to Android Auto from the radio", "☐ instant  ☐ after restart  ☐ black screen"),
        ("Phone call", "☐ OK  ☐ I can't hear  ☐ they can't hear me"),
        ("Steering wheel buttons (track, volume)", "☐ OK  ☐ no"),
        ("Night mode follows the headlights", "☐ yes  ☐ no"),
        ("Automatic return after the reverse camera", "☐ yes  ☐ no"),
        ("Diagnostics › Key frames", ""),
        ("Diagnostics › Honda state", ""),
        ("Diagnostics › Active video decoder", ""),
        ("Notes / exact error messages", "<br><br>"),
    ]
    t = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    return f"""<p>Attach it to your report (a photo is enough): GitHub issue "Rapport de test FK2Droid / Test report" or the XDA
thread "Honda Connect Android System".</p>
<table class="check" style="font-size:9pt"><tr><th>Item</th><th>Result</th></tr>{t}</table>
<p class="small">FK2Droid {VER} · minSdk 15 (Android 4.0.4) · package <code>com.fk2droid</code> · supported dongles: USB
1314:1520 and 1314:1521 · signed with the FK2Play key (SHA-256 8D:F7:C2:BD…D6:CC:29:26). Honda Permissions is an unofficial
community tool: neither its author nor I can guarantee it is risk-free for the head unit. Android Auto is a trademark of
Google LLC. Not affiliated with Google, Honda or Carlinkit.</p>
<p class="small" style="font-size:7.8pt;margin:0">Thanks: MaKi83 (OpenDroidAuto) for the hardware video decoder, the steering wheel service and the day/night and
camera reading; S_Mike for Honda Permissions; the node-carplay / pycarplay community for documenting the dongle protocol;
the members of the XDA thread "Honda Connect Android System".</p>"""


SAFETY = """<div class="box stop"><b>Safety.</b> Do everything while parked, handbrake on, engine running (the battery must not
run low during an install). Never switch the ignition off during an install. Do not use the screen while driving. Allow
about 30 minutes (10 minutes if FK2Play is already installed).</div>"""


def guide_rc3():
    b = news() + f"""<div class="pb"></div>
<h1>Installing Android Auto on an RC3 Honda Connect</h1>
<div class="sub">Civic FK2 / Type R, HR-V, CR-V, Jazz… · Android 4.0.4 · build <code>09.08C.00.xxxx</code> (RC3) ·
Carlinkit CPC200-CCPA dongle · FK2Droid {VER} · {DATE}</div>
<div class="box info">This guide is for <b>RC3</b> only (build <code>09.08C.00.xxxx</code>, for example <code>09.08C.00.1123</code>
with main software <code>31.00.cf</code>). For another version, use the "all versions" guide.</div>
{SAFETY}
<h3>Contents</h3>
<div class="toc"><ol>
<li>How it works</li><li>What you need</li><li>Check that you are on RC3</li><li>Install Honda Permissions</li>
<li>Install FK2Droid</li><li>Give FK2Droid its rights</li><li>FK2Play and FK2Droid together</li>
<li>Test 1: without the dongle</li><li>Test 2: plug in the dongle</li><li>Test 3: connect the Android phone</li>
<li>FK2Droid settings</li><li>Troubleshooting</li><li>What not to do · going back</li><li>Results sheet</li>
</ol></div>
<div class="box ok"><b>Shortcut if FK2Play already works in your car:</b> steps 5, 6, 7, then 9 and 10 (Honda Permissions,
the dongle and HandsFreeLink are already set up).</div>
<h2>1. How it works</h2>{diagram()}
<h2>2. What you need</h2>{needs()}
<h2>3. Check that you are on RC3</h2>{read_build(True)}
<h2>4. Install Honda Permissions</h2>{honda_perms(True)}
<h2>5. Install FK2Droid</h2>{install()}
<h2>6. Give FK2Droid its rights</h2>{rights()}
<h2>7. FK2Play and FK2Droid together</h2>{together()}
<h2>8. Test 1: without the dongle</h2>{test1()}
<h2>9. Test 2: plug in the dongle</h2>{test2()}
<h2>10. Test 3: connect the Android phone</h2>{test3()}
<h2>11. FK2Droid settings</h2>{settings()}
<h2>12. Troubleshooting</h2>{trouble()}
<h2>13. What not to do</h2>{donts()}
<div class="pb"></div><h2>14. Results sheet</h2>{sheet()}
"""
    return html("RC3 user guide", b)


def guide_all():
    b = news() + f"""<div class="pb"></div>
<h1>FK2Droid — user guide, all versions</h1>
<div class="sub">Android Auto on the Honda Connect gen 1 (Android 4.0.4) with a Carlinkit CPC200-CCPA dongle · RC3 to RC8 ·
FK2Droid {VER} · {DATE}</div>
{SAFETY}
<div class="box ok"><b>If FK2Play already works in your car:</b> Honda Permissions is in place whatever your RC. Go straight to
steps 4, 5 and 6, then 7 to 9.</div>
<h2>1. How it works and what you need</h2>{diagram()}{needs()}
<h2>2. Note the Honda Connect version (build)</h2>{read_build(False)}
<h2>3. Install Honda Permissions (once)</h2>{honda_perms(False)}
<h2>4. Install FK2Droid</h2>{install()}
<h2>5. Set FK2Droid up in Honda Permissions</h2>{rights()}
<h2>6. FK2Play and FK2Droid together</h2>{together()}
<h2>7. Test 1 — without the dongle</h2>{test1()}
<h2>8. Test 2 — plug in the dongle</h2>{test2()}
<h2>9. Test 3 — connect the Android phone</h2>{test3()}
<h2>10. Settings</h2>{settings()}
<h2>11. Troubleshooting</h2>{trouble()}
<h2>12. What not to do · going back</h2>{donts()}
<div class="pb"></div><h2>Results sheet</h2>{sheet()}
"""
    return html("All versions user guide", b)


if __name__ == "__main__":
    for name, fn in (("User_guide_FK2Droid_RC3", guide_rc3), ("User_guide_FK2Droid_all_versions", guide_all)):
        with open(os.path.join(HERE, name + ".html"), "w", encoding="utf-8") as f:
            f.write(fn())
    print("HTML ok")
