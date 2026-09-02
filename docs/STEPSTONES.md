# Neurosonic Stepstones

Ky dokument përkufizon milestone-at e ekzekutimit me rezultate të matshme.

## S1 — Foundation Stability

**Objective:** runtime i qëndrueshëm pa ndërprerje kritike.

- Port cleanup i automatizuar (`8080`, `8000`, `5500`)
- Health checks aktive
- Incident triage i dokumentuar

**Success Criteria:** 7 ditë pa crash kritik në startup.

## S2 — Dynamic Product Layer

**Objective:** UI/Plugin layer i gatshëm për përdorues realë.

- UI Composer aktiv
- Plugin attach/list funksional
- Consent flags (`liability_ack`, `sensitive_data_ack`) të detyrueshme sipas scope

**Success Criteria:** 95% success-rate për flow-et bazë API.

## S3 — User Ownership First

**Objective:** përdoruesi kontrollon data-n dhe portability.

- Profili ruhet lokal (`personal_node/profiles`)
- Git export në repo të user-it
- Path-validation dhe contract boundary të qarta

**Success Criteria:** 100% kalim i testeve të eksportit në Git.

## S4 — Release Discipline

**Objective:** çdo ndryshim i rëndësishëm të dalë me standard release-i.

- Changelog i përditësuar
- Semantic tag (`vX.Y.Z`)
- GitHub release me notes

**Success Criteria:** çdo release ka audit trail të plotë.

## S5 — Governance and Scale

**Objective:** rritje pa kompromentuar DNA-në immutable.

- Rishikim mujor i politikave
- Raporte krahasuese release-over-release
- Prioritizim backlog nga metrika reale

**Success Criteria:** > 85 pikë në scorecard mujore.
