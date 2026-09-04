# Tracing Uniform Standard

## Scope

This standard applies to API responses, internal pipeline events, and audit records.

## Required Fields

- `trace.trace_id`: unique request/session trace identifier (hex string, 16-64 chars)
- `trace.input_hash`: SHA-256 hash for normalized input payload
- `trace.output_hash`: SHA-256 hash for normalized output payload
- `timestamp`: UTC epoch timestamp
- `component`: logical producer (`ui.prompt`, `thinking`, `bridge`, `policy`)
- `status`: `completed`, `failed`, or `degraded`

## Response Contract

For `/api/shell/think`, responses must include:

- top-level `trace` object with `trace.trace_id`, `trace.input_hash`, `trace.output_hash`
- `verification.reasoning_validated`
- `trace.pipeline[]` where each step includes `component`, `status`, `duration_ms`, `input_hash`, `output_hash`

Optional forward-compatible field:

- top-level `trace_id` as shortcut mirror of `trace.trace_id`

## Correlation Rules

- Keep one stable `trace_id` for all steps in one request.
- Log `input_hash` before external processing begins.
- Log `output_hash` immediately before returning the response.
- On failures, keep trace fields present even if response content is partial.

## Validation

Run:

```bash
python scripts/trace_uniform_check.py --base-url http://127.0.0.1:8000
```

This check validates trace field presence and shape against a running backend. It
does not replace bridge results or fabricate a response; an unavailable backend
is a failed check.
