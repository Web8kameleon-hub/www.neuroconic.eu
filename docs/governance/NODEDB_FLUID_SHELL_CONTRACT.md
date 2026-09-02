# NodeDB Fluid Shell Contract

Ky dokument definon kontratën operacionale për shell-in Neurosonic me konceptin `NodeDB Fluid`, pa mock dhe me minimizim konfliktesh mes gjuhëve/programeve.

## Objektivi

- Shell-i (`Python`, `npm`, `crates`) duhet të përdorë vetëm endpoint-et reale `GET /api/health` dhe `POST /api/shell/think`.
- `NodeDB Fluid` mbetet burimi kanonik për gjendje/metadata, jo cache të sajuara në klient.
- Në mungesë shërbimi, rezultati duhet të jetë vetëm `service unavailable`, jo përgjigje të simuluar.

## A është e mundur zero konflikt absolut?

Garanci absolute $100\%$ për “kurrë konflikt” nuk ekziston në sisteme heterogjene.

Praktikisht arrihet një model **near-zero conflict** me këto rregulla:

- Një kontratë unike JSON për payload-et e shell-it.
- Një fjalor i përbashkët termash (`engine`, `prompt`, `response`, `hash`, `metadata`).
- Versionim i kontratës (`schema_version`) dhe kompatibilitet mbrapa.
- Teste cross-language para merge (`Python` + `Node.js` + `Rust`) mbi të njëjtin backend real.
- Commit-e të kontrolluara me scope të ngushtë dhe rollback të thjeshtë.

## Guardrails kundër regresit

- Çdo ndryshim shell/API të kalojë smoke-check real te `/api/health` dhe `/api/shell/think`.
- Ndalohet ndryshimi i emrave të fushave pa bump versioni të kontratës.
- Ndalohet futja e “compat shims” që fshehin gabime reale.
- Në CI: fail nëse mungon `schema_version` ose prishet deserializimi në një nga klientët.

## Komit i kontrolluar

Strategjia e rekomanduar:

1. Ndrysho vetëm një domain (`docs`, `shell`, `api`) për commit.
2. Ekzekuto check-et minimale para commit.
3. Commit message me prefiks të qartë (`docs:`, `fix:`, `feat:`).
4. Ruaj changelog të shkurtër për kontratën e shell-it.
