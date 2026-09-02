use anyhow::{anyhow, Result};
use reqwest::blocking::Client;
use serde_json::{json, Value};

pub const DEFAULT_API_BASE: &str = "http://127.0.0.1:8000";

fn normalize_base(api_base: &str) -> String {
    api_base.trim_end_matches('/').to_string()
}

pub fn health(api_base: &str) -> Result<Value> {
    let base = normalize_base(api_base);
    let client = Client::new();
    let response = client
        .get(format!("{base}/api/health"))
        .send()?
        .error_for_status()?;
    let body = response.json::<Value>()?;
    Ok(body)
}

pub fn think(api_base: &str, prompt: &str, engine: &str) -> Result<Value> {
    let base = normalize_base(api_base);
    let client = Client::new();
    let response = client
        .post(format!("{base}/api/shell/think"))
        .json(&json!({"prompt": prompt, "engine": engine}))
        .send()?
        .error_for_status()?;
    let body = response.json::<Value>()?;
    Ok(body)
}

pub fn extract_response_text(payload: &Value) -> Result<String> {
    if payload
        .get("success")
        .and_then(Value::as_bool)
        .is_some_and(|ok| !ok)
    {
        let message = payload
            .get("error")
            .and_then(Value::as_str)
            .unwrap_or("Service unavailable");
        return Err(anyhow!(message.to_string()));
    }

    Ok(payload
        .get("response")
        .and_then(Value::as_str)
        .unwrap_or_default()
        .to_string())
}
