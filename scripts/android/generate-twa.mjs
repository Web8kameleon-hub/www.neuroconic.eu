#!/usr/bin/env node
/**
 * Generate (or regenerate) the Neurosonic Android TWA (Trusted Web Activity)
 * project from the REAL web app manifest, non-interactively.
 *
 * Uses @bubblewrap/core directly (the same library the official Bubblewrap
 * CLI uses) so the generated Gradle project is standard, not hand-rolled.
 *
 * Why not the `bubblewrap` CLI directly? `bubblewrap init` always prompts
 * interactively (host, name, colors, keystore identity, ...) with no
 * non-interactive flag, which does not work in a CI/automation context.
 * This script performs the equivalent steps without prompts, using either
 * values already present in manifest.webmanifest or explicit overrides
 * below (only for fields the web manifest cannot express, e.g. Android
 * package ID and signing key location).
 *
 * Usage:
 *   node generate-twa.mjs
 *
 * Env vars:
 *   NEUROSONIC_MANIFEST_URL   URL to fetch manifest.webmanifest from.
 *                             Defaults to the production URL. Point this at
 *                             a local server (e.g. http://127.0.0.1:8899/manifest.webmanifest)
 *                             when the production site is not yet updated
 *                             or is unreachable from this environment.
 *   NEUROSONIC_APP_VERSION       Android versionName. Defaults to reading
 *                                __init__.py's __version__.
 *   NEUROSONIC_APP_VERSION_CODE  Android versionCode (integer). Defaults to 1.
 */
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { TwaManifest, TwaGenerator, BufferedLog, ConsoleLog } from '@bubblewrap/core';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..', '..');
const TARGET_DIR = resolve(ROOT, 'packages', 'android', 'neurosonic-twa');
const PACKAGE_ID = 'eu.neurosonic.app';

function readRepoVersion() {
  try {
    const text = readFileSync(resolve(ROOT, '__init__.py'), 'utf-8');
    const match = text.match(/__version__\s*=\s*"([^"]+)"/);
    return match ? match[1] : '1.0.0';
  } catch {
    return '1.0.0';
  }
}

async function main() {
  const manifestUrl = process.env.NEUROSONIC_MANIFEST_URL || 'https://neurosonic.eu/manifest.webmanifest';
  const appVersionName = process.env.NEUROSONIC_APP_VERSION || readRepoVersion();
  const appVersionCode = Number(process.env.NEUROSONIC_APP_VERSION_CODE || 1);

  console.log(`[generate-twa] Reading web manifest from ${manifestUrl}`);
  const twaManifest = await TwaManifest.fromWebManifest(manifestUrl);

  // Overrides not derivable from the web manifest alone.
  twaManifest.packageId = PACKAGE_ID;
  twaManifest.signingKey = { path: './android.keystore', alias: 'neurosonic' };
  twaManifest.enableNotifications = false;
  twaManifest.appVersionName = appVersionName;
  twaManifest.appVersionCode = appVersionCode;
  twaManifest.generatorApp = 'neurosonic-twa-tools';

  const validationError = twaManifest.validate();
  if (validationError) {
    throw new Error(`Invalid TWA manifest: ${validationError}`);
  }

  const generator = new TwaGenerator();
  const log = new BufferedLog(new ConsoleLog('generate-twa'));
  console.log(`[generate-twa] Generating Android project into ${TARGET_DIR}`);
  await generator.createTwaProject(TARGET_DIR, twaManifest, log, () => {});
  log.flush();

  const manifestOutPath = resolve(TARGET_DIR, 'twa-manifest.json');
  await twaManifest.saveToFile(manifestOutPath);
  console.log(`[generate-twa] Wrote ${manifestOutPath}`);
  console.log('[generate-twa] Done. Next steps:');
  console.log('  1. Generate/confirm a signing keystore (see README.md).');
  console.log('  2. Run scripts/android/generate_assetlinks.mjs to produce .well-known/assetlinks.json.');
  console.log('  3. Build with ./gradlew assembleRelease (or bundleRelease) inside the project.');
}

main().catch((err) => {
  console.error('[generate-twa] FAILED:', err);
  process.exitCode = 1;
});
