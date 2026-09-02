# Threat Model (STRIDE)

## Metadata

- System: `www.neurosonic.eu`
- Version: `v1`
- Review Date: `2026-09-02`
- Method: STRIDE with risk register

## Assets

- User prompts and response payloads
- Trace/audit metadata (`trace_id`, `input_hash`, `output_hash`)
- Plugin profile configuration and metadata
- Runtime integrity policies and guardrail outputs
- Release artifacts and CI workflows

## Trust Boundaries

1. Client browser ↔ FastAPI backend
2. Backend ↔ bridge/runtime engine
3. Backend ↔ plugin URLs (egress boundary)
4. CI pipeline ↔ repository and release tags

## STRIDE Register

| ID | Category | Threat | Entry Point | Existing Control | Residual Risk | Required Action |
| --- | --- | --- | --- | --- | --- | --- |
| TM-001 | Spoofing | Forged client requests without identity context | `/api/*` | Internal auth pathways, policy checks | Medium | Add stronger auth profile for production endpoints |
| TM-002 | Tampering | Response payload manipulation in transit | HTTP response path | Hashes in verification metadata | Medium | Enforce TLS everywhere and signed audit bundles |
| TM-003 | Repudiation | Actor denies a high-impact request | request lifecycle | `trace_id` + hash traces | Medium | Persist immutable audit sink with retention policy |
| TM-004 | Information Disclosure | Sensitive fields leaked via plugin metadata | `/api/ui/plugins/{profile_id}` | Sensitive key rejection in API | Low-Medium | Expand denylist and add structured secret scanner |
| TM-005 | Denial of Service | Request flood or oversized prompts | `/api/shell/think` | Validation and no-fake checks | Medium-High | Add rate limiting and adaptive concurrency guards |
| TM-006 | Elevation of Privilege | Unsafe plugin URL reaches private network | plugin attach endpoint | Private/local network block | Medium | Add outbound allowlist and DNS pinning |
| TM-007 | Supply Chain | Compromised dependency/release artifact | CI/release process | guardrails + immutable release workflow | Medium | Add artifact signing and provenance attestation |

## Risk Scoring

Use score = Likelihood (1-5) × Impact (1-5).

- Low: 1-6
- Medium: 7-12
- High: 13-19
- Critical: 20-25

## Review Cadence

- Full review every release minor version.
- Mandatory review after security incident.
- Update threats when new external integrations are introduced.

## Evidence Links

- `docs/production/canonical/repo_integrity_guard_report.json`
- `docs/production/canonical/routes_history_guard_report.json`
- `docs/production/evidence/benchmark_compare_latest.json`
- `docs/production/observability/SLO_DEFINITIONS.json`
