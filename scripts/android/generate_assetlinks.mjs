#!/usr/bin/env node
/**
 * Generates `.well-known/assetlinks.json` (Digital Asset Links) for the
 * Neurosonic TWA, from the REAL SHA256 certificate fingerprint of a signing
 * keystore -- never a placeholder/invented fingerprint.
 *
 * Usage:
 *   node generate_assetlinks.mjs <path-to-keystore> <alias> <storepass>
 *
 * Example (dev keystore created per README.md):
 *   node generate_assetlinks.mjs ../../packages/android/neurosonic-twa/android.keystore neurosonic changeit
 *
 * Output:
 *   Writes <repo-root>/.well-known/assetlinks.json, which must be deployed
 *   and served at https://neurosonic.eu/.well-known/assetlinks.json for
 *   Android to verify the TWA's Digital Asset Link.
 *
 * IMPORTANT: Re-run this whenever the signing key changes (e.g. switching
 * from a local dev keystore to the real Play Store release/upload key), and
 * redeploy the site so the fingerprint served matches the APK/AAB actually
 * being installed. A stale fingerprint here means Chrome will show the TWA
 * with browser UI (address bar) instead of a trusted full-screen app.
 */
import { execFileSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { DigitalAssetLinks } from '@bubblewrap/core';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..', '..');
const PACKAGE_ID = 'eu.neurosonic.app';

function extractSha256Fingerprint(keytoolOutput) {
  const match = keytoolOutput.match(/SHA256:\s*([0-9A-Fa-f:]+)/);
  if (!match) {
    throw new Error('Could not find a SHA256 fingerprint in keytool output.');
  }
  return match[1].toUpperCase();
}

function main() {
  const [, , keystorePath, alias, storepass] = process.argv;
  if (!keystorePath || !alias || !storepass) {
    console.error('Usage: node generate_assetlinks.mjs <keystore> <alias> <storepass>');
    process.exit(2);
  }

  const output = execFileSync('keytool', [
    '-list', '-v',
    '-keystore', keystorePath,
    '-alias', alias,
    '-storepass', storepass,
  ], { encoding: 'utf-8' });

  const fingerprint = extractSha256Fingerprint(output);
  console.log(`[generate-assetlinks] Real SHA256 fingerprint: ${fingerprint}`);

  const json = DigitalAssetLinks.generateAssetLinks(PACKAGE_ID, fingerprint);
  const outDir = resolve(ROOT, '.well-known');
  mkdirSync(outDir, { recursive: true });
  const outPath = resolve(outDir, 'assetlinks.json');
  writeFileSync(outPath, json);
  console.log(`[generate-assetlinks] Wrote ${outPath}`);
  console.log('[generate-assetlinks] Deploy this file so it is served at');
  console.log('  https://neurosonic.eu/.well-known/assetlinks.json');
}

main();
