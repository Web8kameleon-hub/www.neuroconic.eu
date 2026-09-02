# @web8kameleon-hub/neurosonic-shell

Real-service shell/client for Neurosonic backend (`no mock`).

## Install

```bash
npm install -g @web8kameleon-hub/neurosonic-shell
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

## JavaScript API

```js
import { health, think } from "@web8kameleon-hub/neurosonic-shell";

const h = await health();
const r = await think("pershkruaj hvo memory", { engine: "hybrid" });
```

Requires a running Neurosonic backend exposing:

- `GET /api/health`
- `POST /api/shell/think`
