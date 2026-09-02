# Structure Consolidation Plan

## Goal

Reduce top-level sprawl without breaking existing entrypoints, scripts, or published interfaces.

## Current Risks

- Mixed top-level modules (`neurosonic_*.py`, `clx*`, `backend/`, `src/`) increase discovery and ownership ambiguity.
- Production and governance artifacts are spread between `docs/`, `scripts/`, and root.
- Multiple public execution paths make support and onboarding harder.

## Target Shape (Phased)

- Keep compatibility wrappers at root for existing users.
- Move implementation ownership under `src/neurosonic/` by domain.
- Treat root as a thin integration layer (entrypoints + release metadata).

## Domain Map

- `src/neurosonic/core/`: runtime bootstrapping, compatibility primitives.
- `src/neurosonic/ai/`: thinking pipeline and reasoning adapters.
- `src/neurosonic/security/`: no-fake, plugin safety checks, policy hooks.
- `src/neurosonic/api/`: API-facing contracts shared with `backend/`.
- `src/neurosonic/bridge/`: Lightning bridge and external protocol connectors.
- `src/neurosonic/governance/`: policy profiles, guardrail rule definitions.

## Migration Sequence

1. Add internal package paths in parallel with current modules.
2. Refactor imports inside tests/scripts first; preserve public filenames at root.
3. Add deprecation notices in docs for old internal import paths.
4. Consolidate CI checks to enforce only one canonical implementation path per domain.
5. After 2 stable releases, remove duplicated internals and keep wrappers only if needed.

## Acceptance Criteria

- Existing commands remain valid (`python neurosonic.py`, benchmark scripts, guardrails).
- CI and guardrails pass with no regression in benchmark pass-rate.
- Production evidence artifacts continue to generate under `docs/production/evidence`.
