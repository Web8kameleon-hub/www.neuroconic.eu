# Hostimi i Neurosonic Trinity+ASI

Stack-u production ka tri shërbime: `web` (Nginx publik), `backend` (FastAPI
privat) dhe `lightning-spp` (motori SPP privat).

## Kërkesat dhe nisja

Kërkohet Linux me Docker Engine 26+, Docker Compose v2, 2 CPU, 2 GB RAM, 10 GB
disk dhe një domain me TLS.

```bash
git clone https://github.com/LedjanAhmati/www.neuroconic.eu.git
cd www.neuroconic.eu
cp .env.example .env
docker compose config
docker compose build --pull
docker compose up -d
docker compose ps
```

```bash
curl --fail http://127.0.0.1/healthz
curl --fail http://127.0.0.1/api/health
curl --fail http://127.0.0.1/api/shell/health
```

Dashboard-i gjendet te `/neurosonic_dashboard.html` dhe përdor API-n në të
njëjtin origin përmes Nginx.

## Domain dhe HTTPS

Compose ekspozon `${HTTP_PORT:-80}` dhe `${HTTPS_PORT:-443}`. Nginx brenda
kontejnerit `web` terminon vetë TLS-në në 443 (porta 80 kthen vetëm `/healthz`
dhe ridrejton pjesën tjetër në HTTPS). Mos publiko portat `8000` ose `8080`.

### TLS me Cloudflare (Origin Certificate)

Kur domain-i është proxied në Cloudflare (orange cloud), rekomandohet modaliteti
`Full (strict)` në SSL/TLS + një Origin Certificate në origin:

```bash
mkdir -p deploy/certs
openssl req -new -newkey rsa:2048 -nodes \
  -keyout deploy/certs/origin.key -out deploy/certs/origin.csr \
  -subj "/CN=neurosonic.eu" \
  -addext "subjectAltName=DNS:neurosonic.eu,DNS:*.neurosonic.eu"
```

Ngjit `origin.csr` te Cloudflare Dashboard → SSL/TLS → Origin Server →
Create Certificate → "Use my private key and CSR", ruaj PEM-in e kthyer si
`deploy/certs/origin.pem`. Vendos SSL/TLS mode në `Full (strict)`.

`origin.key`/`origin.pem`/`origin.csr` janë në `.gitignore` — mos i commit
kurrë. Restart `web` pas ndryshimit të certifikatave:

```bash
docker compose up -d --force-recreate web
```

### Alternativë: reverse proxy tjetër

Nëse preferon Caddy, Traefik ose Nginx Proxy Manager përpara stack-ut (p.sh.
kur domain-i nuk kalon nga Cloudflare), vendos `HTTPS_PORT` në një portë tjetër
ose lëre proxy-n të flasë me origin-in vetëm në `HTTP_PORT`:

```caddyfile
neurosonic.eu, www.neurosonic.eu {
    reverse_proxy 127.0.0.1:80
}
```

```dotenv
HTTP_PORT=8088
CORS_ORIGINS=https://neurosonic.eu,https://www.neurosonic.eu
```

Kufizo portën alternative me firewall.

## Persistenca dhe backup

Të dhënat ruhen në `neurosonic_spp-memory`, `neurosonic_backend-memory` dhe
`neurosonic_backend-logs`.

```bash
mkdir -p backups
docker run --rm -v neurosonic_spp-memory:/data:ro -v "$PWD/backups:/backup" alpine \
  tar czf /backup/spp-memory.tar.gz -C /data .
docker run --rm -v neurosonic_backend-memory:/data:ro -v "$PWD/backups:/backup" alpine \
  tar czf /backup/backend-memory.tar.gz -C /data .
```

Ruaji backup-et të enkriptuara dhe provo rikthimin periodikisht.

## Përditësimi dhe rollback

```bash
git pull --ff-only
docker compose build --pull
docker compose up -d --remove-orphans
docker compose ps
```

Për rollback, checkout tag-un/commit-in e mëparshëm dhe rindërto. Merr backup
para ndryshimeve që prekin formatin e të dhënave.

## Platforma të menaxhuara

Në Render, Railway, Fly.io, Azure Container Apps ose Kubernetes përdor të njëjtat
tri imazhe. Backend-i kërkon `LIGHTNING_SPP_URL=http://<spp-service>:8080`; vetëm
web-i duhet të ketë ingress publik. Health paths janë `/healthz`, `/api/health`
dhe `/health` përkatësisht.
