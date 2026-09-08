# Experiment Plan (30 Days)

Qëllimi: verifikim praktik i sistemit për `Zero Fake`, arsyetim, memorie, siguri dhe operim.

## Java 1 — Baseline dhe Integritet

### Objektiva (Java 1)

- Fikso versionin (`tag` ose `commit SHA`) për të gjitha testet.
- Verifiko endpoint-et kyçe dhe trace contract.
- Ndërto dataset fillestar për testet faktike/policy.

### Ekzekutim (Java 1)

1. Run `scripts/trace_uniform_check.py` kundër backend-it live.
2. Gjenero evidence pack (`production_evidence_pack`, `observability_slo_snapshot`).
3. Plotëso rreshtat fillestarë në `METRICS_SCORECARD_TEMPLATE.csv`.

### Kriter pranimi (Java 1)

- Trace contract pass.
- Artefaktet e evidencës të gjeneruara pa gabime.

## Java 2 — Zero Fake / Hallucination

### Objektiva (Java 2)

- Testo factual grounding, policy conflicts, prompt injection.
- Mat pass-rate, critical failures, dhe consistency.

### Ekzekutim (Java 2)

1. Ekzekuto suite sipas `ZERO_FAKE_HALLUCINATION_CHECKLIST.md`.
2. Regjistro për çdo test: input, output, verification flags.
3. Përditëso scorecard input JSON me nota të mbështetura në evidencë.

### Kriter pranimi (Java 2)

- 0 critical failures.
- >= 90% pass-rate total për suite.

## Java 3 — Memorie dhe Arsyetim i gjatë

### Objektiva (Java 3)

- Mat sa mirë ruhet konteksti afatgjatë.
- Mat cilësinë e vendimmarrjes me rregulla dhe grafe.

### Ekzekutim (Java 3)

1. Skenarë me 10-20 kthesa bisede (multi-turn).
2. Testo retrieval correctness nga memorie (fakte të hershme në bisedë).
3. Krahaso cilësinë me të paktën 2 alternativa (baseline model/tool).

### Kriter pranimi (Java 3)

- Long-context retention >= 85%.
- Reasoning validated >= 90% në skenarët e policy conflict.

## Java 4 — Operim, Siguri, Vendim

### Objektiva (Java 4)

- Rollback drill i dokumentuar.
- Kontroll i GDPR/ligjor + hard gates.
- Llogarit vendimin final me scorecard.

### Ekzekutim (Java 4)

1. Simulo një deploy + rollback dhe mat RTO/RPO.
2. Verifiko statusin e hard gates në `scorecard_input`.
3. Ekzekuto `scripts/assessment_scorecard.py` dhe arkivo raportin.

### Kriter pranimi (Java 4)

- Të gjitha hard gates `true` për vendim `Go`/`Conditional`.
- Raport final me vendim dhe plan remedimi për boshllëqet.

## Raportimi javor

Çdo javë publiko:

- Summary (1 faqe): çfarë kaloi/çfarë dështoi.
- CSV i përditësuar i metrikave.
- 3 rreziqet kryesore + veprimet korrigjuese.
