# Error Budget Policy

## Objective

Define a consistent policy for burn-rate decisions using 30-day SLO windows.

## Budget Formula

For an SLO of $99.5\%$, the monthly error budget is:

$$
error\_budget = 1 - 0.995 = 0.005 = 0.5\%
$$

## Burn Thresholds

- **Healthy**: burn-rate < 0.50x (feature delivery normal)
- **Warning**: burn-rate between 0.50x and 1.00x (release caution)
- **Critical**: burn-rate > 1.00x (freeze non-critical releases)

## Operational Actions

- **Healthy**: continue roadmap and monitor daily.
- **Warning**: require rollback plan review before releases.
- **Critical**: stop risky deploys, run incident response, and require mitigation evidence.

## Evidence Sources

- `docs/production/evidence/availability_trend.json`
- `docs/production/evidence/latency_trend.json`
- `docs/production/evidence/slo_snapshot_latest.json`
