# Incident Log

Track only real incidents with timestamps, impact, root cause, and corrective actions.

| Date (UTC) | Severity | Summary | Impact | Root Cause | Corrective Action | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-05 (commit `2a4c94d`, 18:19:51Z) | Medium | Accidental removal of `backend_b` failover service | Backend pool reduced from 2 to 1 instance behind Nginx (`neurosonic_backend_pool`); loss of failover/rolling-update redundancy for `backend`/`backend_b` | Refactor commit removed `backend_b` from `docker-compose.yml`, `deploy/nginx.conf`, `scripts/guardrails/compose.services.txt`, and simultaneously relaxed `scripts/guardrails/repo_integrity_guard.py` required-service list, so CI guardrails passed despite the reduced topology | Reverted in commit `edaf073` (2026-09-06): restored `backend_b` across compose/nginx/guardrails/rolling-update scripts/docs; guardrail required-list restored so future removal fails CI; see `docs/releases/v1.0.16.md` | Closed |
