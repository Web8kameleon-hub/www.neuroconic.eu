const DEFAULT_API_BASE = "http://127.0.0.1:8000";

function normalizeBase(apiBase = DEFAULT_API_BASE) {
  return apiBase.endsWith("/") ? apiBase.slice(0, -1) : apiBase;
}

export async function health(apiBase = DEFAULT_API_BASE) {
  const response = await fetch(`${normalizeBase(apiBase)}/api/health`, {
    method: "GET",
    headers: { Accept: "application/json" }
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

export async function think(prompt, options = {}) {
  const apiBase = normalizeBase(options.apiBase || DEFAULT_API_BASE);
  const engine = options.engine || "hybrid";
  const response = await fetch(`${apiBase}/api/shell/think`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json"
    },
    body: JSON.stringify({ prompt, engine })
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return response.json();
}
