# Neurosonic Android TWA (Trusted Web Activity)

Wraps <https://neurosonic.eu> as an installable Android app using a
[Trusted Web Activity](https://developer.chrome.com/docs/android/trusted-web-activity/)
(the site opens full-screen, without browser chrome, once Digital Asset
Links verification succeeds). This is the standard way to publish a
production PWA to the Google Play Store without maintaining a separate
native codebase.

- Package (application) ID: `eu.neurosonic.app`
- Host: `neurosonic.eu`
- Generated with [`@bubblewrap/core`](https://www.npmjs.com/package/@bubblewrap/core)
  (the same library behind the official `bubblewrap` CLI), driven
  non-interactively by `scripts/android/generate-twa.mjs`.

## What is committed vs. generated vs. gitignored

| Path | Status |
| --- | --- |
| `app/`, `build.gradle`, `settings.gradle`, `gradle*`, `twa-manifest.json`, `store_icon.png` | Committed (regenerable) |
| `.gradle/`, `build/`, `app/build/` | Gitignored build output |
| `android.keystore` (or any `*.keystore` / `*.jks`) | **Gitignored, never committed** -- see [Signing](#signing) |
| `../../.well-known/assetlinks.json` | Committed, but tied to whichever keystore last generated it -- see [Digital Asset Links](#digital-asset-links-wellknownassetlinksjson) |

## Regenerating the project

The Gradle project is derived entirely from the real
[`manifest.webmanifest`](/manifest.webmanifest) at the repo root, plus a
couple of Android-only fields Bubblewrap cannot infer from a web manifest
(package ID, signing key location). To regenerate after changing the web
manifest or bumping the app version:

```powershell
cd scripts/android
npm install
# Point at the live site once it serves the updated manifest/icons:
$env:NEUROSONIC_MANIFEST_URL = "https://neurosonic.eu/manifest.webmanifest"
$env:NEUROSONIC_APP_VERSION_CODE = "2"   # bump every release
node generate-twa.mjs
```

If the production site does not yet serve the updated manifest (e.g. you
changed `manifest.webmanifest` locally and haven't deployed), serve the
repo root locally first and point the script at it instead:

```powershell
# From the repo root, in a separate terminal:
python -m http.server 8899 --bind 127.0.0.1

# Then, in scripts/android:
$env:NEUROSONIC_MANIFEST_URL = "http://127.0.0.1:8899/manifest.webmanifest"
node generate-twa.mjs
```

After generation, `packages/android/neurosonic-twa/twa-manifest.json` and
`app/build.gradle`/`app/src/main/res/values/strings.xml` will contain
whatever host you pointed the generator at -- if you used the local
server, replace `127.0.0.1:8899` with `neurosonic.eu` (and `http://` with
`https://`) in those 3 files before committing. This repository's copy
already targets the real production host.

## Building

Requires JDK 17 and the Android SDK (`ANDROID_HOME`/`JAVA_HOME` set).

```powershell
cd packages/android/neurosonic-twa
$env:JAVA_HOME = "<path to a JDK 17 install>"
$env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk"
.\gradlew.bat assembleDebug     # unsigned/debug-signed APK for local testing
.\gradlew.bat bundleRelease     # signed AAB for Play Store upload (needs the keystore, see below)
```

Debug builds are signed with a Gradle-generated debug key automatically
and do not require the release keystore.

## Signing

**Never commit a signing keystore or its password.** `*.keystore` and
`*.jks` are gitignored repo-wide.

### Local/dev keystore (for testing `assembleDebug`/`bundleRelease` locally)

```powershell
cd packages/android/neurosonic-twa
keytool -genkeypair -v -keystore android.keystore -alias neurosonic `
  -keyalg RSA -keysize 2048 -validity 10000 `
  -storepass "<choose-a-strong-password>" -keypass "<same-or-different>" `
  -dname "CN=Neurosonic Dev, OU=Web8kameleon-hub, O=ABA GmbH, C=DE"
```

### Production/Play Store release keystore

Generate a **separate**, securely stored keystore for the real release
(never reuse the dev key). Store the file and passwords in a secrets
manager or offline backup -- losing it means losing the ability to publish
updates to the same Play Store listing. Use Google Play App Signing so
Google also holds a copy for recovery.

## Digital Asset Links (`/.well-known/assetlinks.json`)

Android only removes the browser chrome (full trusted mode) if
`https://neurosonic.eu/.well-known/assetlinks.json` lists the SHA256
certificate fingerprint of the key that signed the installed APK/AAB.

Regenerate it from a real keystore's real fingerprint (never hand-write a
fingerprint):

```powershell
cd scripts/android
$env:PATH = "<jdk17>\bin;$env:PATH"   # keytool must be on PATH
node generate_assetlinks.mjs ..\..\packages\android\neurosonic-twa\android.keystore neurosonic <storepass>
```

This writes `<repo-root>/.well-known/assetlinks.json`, which is deployed by
`Dockerfile.frontend` and served by `deploy/nginx.conf` at
`/.well-known/assetlinks.json` with `Content-Type: application/json`.

**Before submitting to Google Play:** regenerate this file using the real
release keystore's fingerprint (not the dev keystore), and after the first
upload, add Google Play App Signing's fingerprint (shown in Play
Console -> Setup -> App integrity) as a **second** entry in the
`sha256_cert_fingerprints` array so both the upload key and Play's
re-signing key are trusted.

## Play Store listing checklist

- [ ] Real release keystore generated and stored securely (not this repo).
- [ ] `assetlinks.json` regenerated with the real release fingerprint(s)
      and deployed (verify with
      `https://developers.google.com/digital-asset-links/tools/generator`).
- [ ] `versionCode`/`versionName` bumped for each release
      (`NEUROSONIC_APP_VERSION_CODE` / repo version) before
      `bundleRelease`.
- [ ] Store listing assets (screenshots, feature graphic, full description)
      prepared in Play Console -- not part of this repo.
- [ ] Privacy policy URL set (can point at `docs/legal/` content once
      published on the site).
- [ ] Content rating questionnaire completed in Play Console.
- [ ] Internal testing track used before any production rollout.

## Troubleshooting

- **App opens with a browser address bar instead of full-screen**: the
  Digital Asset Link isn't verified yet. Confirm
  `https://neurosonic.eu/.well-known/assetlinks.json` is reachable and its
  fingerprint matches the installed APK's signer
  (`keytool -list -v -keystore <ks> -alias <alias>`).
- **`gradlew.bat` fails immediately**: confirm `JAVA_HOME` points at a
  JDK 17 install and `ANDROID_HOME` points at a valid Android SDK with
  `platforms/android-36` and `build-tools` available (Gradle will
  auto-download missing SDK components on first build if licenses are
  accepted).
