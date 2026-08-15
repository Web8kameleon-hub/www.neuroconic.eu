# Checklist para Release/Hosting

## Build

- [ ] Commit-i/tag-u i release-it është identifikuar.
- [ ] Testet dhe `python -m compileall` kalojnë.
- [ ] `docker compose config` kalon.
- [ ] `docker compose build --no-cache` kalon.
- [ ] Nuk ka sekrete, `.env`, databaza ose logje në image/repository.

## Funksionaliteti

- [ ] `/healthz`, `/api/health` dhe `/api/shell/health` kthejnë sukses.
- [ ] Dashboard-i publik nuk dërgon request-e te `localhost`.
- [ ] Compatibility Matrix punon.
- [ ] Scan, Process, Print dhe Pipeline punojnë.
- [ ] Persistenca mbijeton një restart.

## Siguria dhe operimi

- [ ] HTTPS dhe redirect HTTP → HTTPS janë aktive.
- [ ] Portat 8000 dhe 8080 nuk janë publike.
- [ ] `CORS_ORIGINS` ka vetëm domain-et e aprovuara.
- [ ] Firewall, SSH, skanimi i imazheve dhe backup encryption janë verifikuar.
- [ ] Rate limiting/autentikimi janë vendosur për endpoint-et sensitive.
- [ ] Monitorimi, alarmet, backup-i dhe rollback-u janë provuar.
