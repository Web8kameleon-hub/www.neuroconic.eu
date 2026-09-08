# Neurosonic 30-Day Production Scorecard

Ky scorecard e kthen vlerësimin në vendim objektiv **Go / Conditional / No-Go**.

## 1) Kategoritë dhe peshat

| Kategoria | Pesha | Kriteret kryesore |
| --- | ---: | --- |
| Security | 30 | Audit i pavarur, hardening, sekretet, izolimi, incident readiness |
| Privacy & Sovereignty | 20 | Data flow, GDPR, hostim vetjak, DPA/kontrata |
| Reasoning Quality | 20 | Benchmarks të riprodhueshme, krahasim me alternativa |
| Operations & Reliability | 20 | CI/CD, rollback drills, observability, SLO/SLA |
| Documentation & Community | 10 | Dokumentim teknik, roadmap, support channels |

Totali: **100 pikë**.

## 2) Rregullat e vendimit

- **Go**: score total `>= 80` dhe asnjë hard-gate fail.
- **Conditional**: score total `>= 65` dhe asnjë hard-gate fail.
- **No-Go**: score total `< 65` ose çdo hard-gate fail.

## 3) Hard Gates (detyruese)

Nëse ndonjë nga këto është `false`, vendimi bëhet automatikisht **No-Go**:

1. `security_independent_audit_passed`
2. `gdpr_dpa_in_place`
3. `production_release_reproducible`
4. `critical_incident_response_tested`

## 4) Si jepet nota për çdo kategori

Çdo kategori ka sub-kritere me nota `0..5`:

- `0`: mungon plotësisht
- `1`: ad-hoc / pa prova
- `2`: bazike, jo e standardizuar
- `3`: e përdorshme dhe e dokumentuar
- `4`: e fortë, me metrika reale
- `5`: e pjekur, e audituar, e riprodhueshme

Formula për kategori:

`category_score = (average_subscore / 5) * weight`

## 5) Evidencat minimale që duhen ngarkuar

- Security: raport auditimi, listë CVE me status, test izolimi.
- Privacy: data map, retention policy, DPA/ToS, controls për export/delete.
- Quality: benchmark logs + baseline comparison + dataset i përshkruar.
- Operations: release trace, rollback drill log, SLO snapshots.
- Documentation: architecture docs, runbook, roadmap update date.

## 6) Output i pritshëm

Skript-i `scripts/assessment_scorecard.py` prodhon:

- `docs/production/assessment/scorecard_result.json`
- `docs/production/assessment/scorecard_result.md`

## 7) Plan 30-ditor i rekomanduar

- Java 1: Security + privacy baseline dhe hard-gates.
- Java 2: Benchmark krahasues + regressions.
- Java 3: Operim (deploy discipline, rollback drill, observability).
- Java 4: Documentation freeze + vendim Go/No-Go.
