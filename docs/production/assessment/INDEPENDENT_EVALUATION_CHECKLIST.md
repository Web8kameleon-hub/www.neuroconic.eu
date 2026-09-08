# Independent Evaluation Checklist

Përdore këtë checklist për verifikim nga palë e tretë.

## Security

- [ ] Pen-test i jashtëm me raport dhe evidencë remediation.
- [ ] Rishikim i autentikimit/autorizimit për endpoint-et kritike.
- [ ] Verifikim i menaxhimit të sekreteve (jo në repo, jo hardcoded).
- [ ] Test i izolimit midis profileve/tenant-ve/agjentëve.
- [ ] Log audit-i me gjurmueshmëri për veprime kritike.

## Privacy & Sovereignty

- [ ] Data flow diagram për input/output/storage/transfers.
- [ ] GDPR controls (export/delete/retention) të testuara.
- [ ] DPA/kontratat ligjore të dokumentuara.
- [ ] Vetë-hostim i provuar me recovery procedura.

## Reasoning Quality

- [ ] Test set i përcaktuar për use-case kryesor.
- [ ] Baseline kundër të paktën 2 alternativave.
- [ ] Reproducibility run me seed/konfigurim të fiksuar.
- [ ] Raport gabimesh kritike dhe kufij operacionalë.

## Operations & Reliability

- [ ] CI/CD me required checks dhe release trace.
- [ ] Rollback drill i dokumentuar (RTO/RPO).
- [ ] SLO snapshot + error budget status.
- [ ] Incident runbook me role/komunikim/escalation.

## Decision

- [ ] Plotëso `scorecard_input_template.json`.
- [ ] Ekzekuto `scripts/assessment_scorecard.py`.
- [ ] Vendimi final: `Go` / `Conditional` / `No-Go` me nënshkrim të ekipit.
