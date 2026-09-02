use anyhow::Result;
use clap::Parser;
use std::io::{self, Write};

use neurosonic_shell::{extract_response_text, health, think, DEFAULT_API_BASE};

#[derive(Parser, Debug)]
#[command(name = "neurosonic-shell")]
#[command(about = "Real-service Neurosonic shell (no mock).")]
struct Args {
    #[arg(long, default_value = DEFAULT_API_BASE)]
    api_base: String,

    #[arg(long, default_value = "hybrid")]
    engine: String,

    #[arg(long)]
    prompt: Option<String>,

    #[arg(long)]
    health: bool,
}

fn main() -> Result<()> {
    let args = Args::parse();

    if args.health {
        let result = health(&args.api_base)?;
        println!("{}", serde_json::to_string_pretty(&result)?);
        return Ok(());
    }

    if let Some(prompt) = args.prompt {
        let result = think(&args.api_base, &prompt, &args.engine)?;
        println!("{}", serde_json::to_string_pretty(&result)?);
        return Ok(());
    }

    println!("NEUROSONIC Rust shell (real services only)");
    println!("API: {}", args.api_base);
    println!("Commands: /health, /exit\n");

    loop {
        print!("neurosonic> ");
        io::stdout().flush()?;

        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let prompt = input.trim();

        if prompt.is_empty() {
            continue;
        }
        if prompt == "/exit" || prompt == "exit" || prompt == "quit" {
            break;
        }
        if prompt == "/health" {
            match health(&args.api_base) {
                Ok(result) => println!("{}", serde_json::to_string_pretty(&result)?),
                Err(error) => println!("Service unavailable: {error}"),
            }
            continue;
        }

        match think(&args.api_base, prompt, &args.engine) {
            Ok(result) => match extract_response_text(&result) {
                Ok(text) => {
                    println!("{text}");
                    if let Some(hash) = result.get("hash").and_then(|v| v.as_str()) {
                        println!("hash: {hash}");
                    }
                }
                Err(error) => println!("[UNAVAILABLE] {error}"),
            },
            Err(error) => println!("Service unavailable: {error}"),
        }
    }

    Ok(())
}
