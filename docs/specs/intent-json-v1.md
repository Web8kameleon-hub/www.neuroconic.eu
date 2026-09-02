# Intent JSON Spec v1

Specifikim i saktë për kontratën e `Intent` në pipeline-in `shell/think`.

## Scope

- **Producer**: `scanner/intent` faza në backend.
- **Consumer**: `planner`, `memory`, `knowledge`, `reasoning`, `validator`.
- **Transport**: JSON UTF-8, `application/json`.
- **Version**: `intent_schema_version = "1.0"`.

## Intent Object (Canonical)

```json
{
  "intent_id": "int_6f0f0f2a8b3f",
  "intent_schema_version": "1.0",
  "trace_id": "11b9ceabe18d4e53ba5d3c6f528b4bd3",
  "request": {
    "prompt": "Analyze governance policy conflicts",
    "task_type": "reasoning",
    "language": "sq",
    "channel": "api",
    "created_at": "2026-09-02T19:40:00Z"
  },
  "classification": {
    "primary": "governance.analysis",
    "secondary": ["policy.conflict", "compliance"],
    "confidence": 0.84,
    "routing_engine": "clx"
  },
  "constraints": {
    "must_not_echo_input": true,
    "max_latency_ms": 30000,
    "require_verifiable_sources": true,
    "no_fake_gate_required": true
  },
  "plan_hints": {
    "steps_required": ["intent", "planner", "reasoning", "validator"],
    "output_format": "markdown",
    "strictness": "high"
  },
  "integrity": {
    "input_hash": "sha256:...",
    "intent_hash": "sha256:...",
    "source_verified": true
  }
}
```

## JSON Schema (Validation)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://www.neurosonic.eu/specs/intent-json-v1.schema.json",
  "title": "NeurosonicIntentV1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "intent_id",
    "intent_schema_version",
    "trace_id",
    "request",
    "classification",
    "constraints",
    "integrity"
  ],
  "properties": {
    "intent_id": { "type": "string", "pattern": "^int_[a-z0-9]{8,32}$" },
    "intent_schema_version": { "const": "1.0" },
    "trace_id": { "type": "string", "minLength": 16, "maxLength": 64 },
    "request": {
      "type": "object",
      "additionalProperties": false,
      "required": ["prompt", "task_type", "created_at"],
      "properties": {
        "prompt": { "type": "string", "minLength": 1, "maxLength": 20000 },
        "task_type": {
          "type": "string",
          "enum": ["auto", "reasoning", "vision", "code", "text"]
        },
        "language": { "type": "string", "minLength": 2, "maxLength": 16 },
        "channel": { "type": "string", "enum": ["api", "ui", "cli"] },
        "created_at": { "type": "string", "format": "date-time" }
      }
    },
    "classification": {
      "type": "object",
      "additionalProperties": false,
      "required": ["primary", "confidence", "routing_engine"],
      "properties": {
        "primary": { "type": "string", "minLength": 3, "maxLength": 128 },
        "secondary": { "type": "array", "items": { "type": "string" }, "maxItems": 16 },
        "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "routing_engine": { "type": "string", "enum": ["clx", "cli_i", "xcl", "hybrid", "clisonic"] }
      }
    },
    "constraints": {
      "type": "object",
      "additionalProperties": false,
      "required": ["must_not_echo_input", "no_fake_gate_required"],
      "properties": {
        "must_not_echo_input": { "type": "boolean" },
        "max_latency_ms": { "type": "integer", "minimum": 10, "maximum": 120000 },
        "require_verifiable_sources": { "type": "boolean" },
        "no_fake_gate_required": { "type": "boolean" }
      }
    },
    "plan_hints": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "steps_required": { "type": "array", "items": { "type": "string" }, "maxItems": 24 },
        "output_format": { "type": "string", "enum": ["markdown", "json", "text"] },
        "strictness": { "type": "string", "enum": ["low", "medium", "high"] }
      }
    },
    "integrity": {
      "type": "object",
      "additionalProperties": false,
      "required": ["input_hash", "intent_hash", "source_verified"],
      "properties": {
        "input_hash": { "type": "string", "pattern": "^sha256:[A-Fa-f0-9]{64}$" },
        "intent_hash": { "type": "string", "pattern": "^sha256:[A-Fa-f0-9]{64}$" },
        "source_verified": { "type": "boolean" }
      }
    }
  }
}
```

## Runtime Rules

- `task_type=auto` duhet të zgjidhet para `planner`.
- Nëse `constraints.must_not_echo_input=true`, output që barazohet me prompt duhet të shënohet `degraded/failed`.
- `classification.confidence` nuk lejohet hardcoded konstante në kod pa llogaritje reale.
- `integrity.intent_hash` duhet të gjenerohet nga serializim kanonik (`sort_keys=true`, UTF-8).

## Mapping to `/api/shell/think`

- `request.prompt` ↔ request body `prompt`
- `classification.routing_engine` ↔ response `engine/router`
- `constraints.must_not_echo_input` ↔ anti-echo gate
- `integrity.input_hash` ↔ trace `input_hash`

## Rejection Codes

- `INTENT_SCHEMA_INVALID`
- `INTENT_TRACE_MISSING`
- `INTENT_HASH_INVALID`
- `INTENT_CONSTRAINT_VIOLATION`
