#!/usr/bin/env node
import { health, think } from "../lib/client.js";
import { runInteractiveShell } from "../lib/shell.js";

const args = process.argv.slice(2);

function getArg(name, fallback = undefined) {
  const flag = `--${name}`;
  const index = args.indexOf(flag);
  if (index === -1 || index + 1 >= args.length) {
    return fallback;
  }
  return args[index + 1];
}

const apiBase = getArg("api-base", "http://127.0.0.1:8000");
const engine = getArg("engine", "hybrid");
const prompt = getArg("prompt");
const isHealth = args.includes("--health");

if (isHealth) {
  try {
    const result = await health(apiBase);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exit(0);
  } catch (error) {
    process.stderr.write(`Service unavailable: ${error.message}\n`);
    process.exit(2);
  }
}

if (prompt) {
  try {
    const result = await think(prompt, { apiBase, engine });
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exit(0);
  } catch (error) {
    process.stderr.write(`Service unavailable: ${error.message}\n`);
    process.exit(2);
  }
}

await runInteractiveShell(apiBase, engine);
