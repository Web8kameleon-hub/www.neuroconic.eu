import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { health, think } from "./client.js";

export async function runInteractiveShell(apiBase = "http://127.0.0.1:8000", engine = "hybrid") {
  const rl = readline.createInterface({ input, output });

  output.write("NEUROSONIC npm shell (real services only)\n");
  output.write(`API: ${apiBase}\n`);
  output.write("Commands: /health, /exit\n\n");

  try {
    while (true) {
      const prompt = (await rl.question("neurosonic> ")).trim();
      if (!prompt) {
        continue;
      }
      if (prompt === "/exit" || prompt === "exit" || prompt === "quit") {
        break;
      }
      if (prompt === "/health") {
        try {
          const result = await health(apiBase);
          output.write(`${JSON.stringify(result, null, 2)}\n`);
        } catch (error) {
          output.write(`Service unavailable: ${error.message}\n`);
        }
        continue;
      }

      try {
        const result = await think(prompt, { apiBase, engine });
        if (!result.success) {
          output.write(`[UNAVAILABLE] ${result.error || "Service unavailable"}\n`);
          continue;
        }
        output.write(`${result.response || ""}\n`);
        if (result.hash) {
          output.write(`hash: ${result.hash}\n`);
        }
      } catch (error) {
        output.write(`Service unavailable: ${error.message}\n`);
      }
    }
  } finally {
    rl.close();
  }
}
