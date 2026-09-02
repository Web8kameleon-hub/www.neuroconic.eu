# Architecture Snapshot

## Core Contract

- **DNA**: immutable, non-user-editable
- **Genome**: extensible package surface
- **Personal Node**: local-first ownership
- **API Role**: support and orchestration, jo pronësi e kontratave të palëve të treta

## Main Runtime Flows

1. `UI Composer` gjeneron skemë paneli.
2. Profili ruhet lokal në `personal_node/profiles`.
3. Plugin-et lidhen dinamikisht me `liability_ack`.
4. Opsionalisht, profili eksportohet në repo Git të user-it.

## Safety and Liability Boundaries

- Përdoruesi është përgjegjës për subscription/billing/credentials te shërbimet e palëve të treta.
- Neurosonic është **api-support-only** në integrime jashtë platformës.

## Suggested Architecture Reviews

- Weekly architecture check (30 min)
- Monthly governance check (60 min)
- Release-by-release compatibility report
