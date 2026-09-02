# neurosonic-shell (Rust)

Real-service shell/client for Neurosonic backend (`no mock`).

## Install

```bash
cargo install neurosonic-shell
```

## Usage

```bash
neurosonic-shell --health
neurosonic-shell --prompt "pershkruaj hvo memory"
neurosonic-shell
```

Optional flags:

- `--api-base http://127.0.0.1:8000`
- `--engine hybrid`

Requires a running Neurosonic backend exposing:

- `GET /api/health`
- `POST /api/shell/think`
