# Runbook Operacional

## Gjendja dhe logjet

```bash
docker compose ps
docker compose logs --tail=100 web backend lightning-spp
curl --fail https://neurosonic.eu/healthz
curl --fail https://neurosonic.eu/api/health
curl --fail https://neurosonic.eu/api/shell/health
```

Deploy-i është i shëndetshëm kur tre container-at janë `healthy`, API kthen
`status: healthy` dhe `lightning_spp.status` është `active`.

```bash
docker compose logs -f --tail=200
docker compose restart backend
docker compose build --pull
docker compose up -d --remove-orphans
docker stats
docker system df
```

## API jep 502

Kontrollo backend-in dhe provo health endpoint-in brenda container-it:

```bash
docker compose exec backend python -c \
  "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/api/health').read().decode())"
```

## Lightning është inactive

```bash
docker compose logs --tail=200 lightning-spp
docker compose exec backend python -c \
  "import urllib.request; print(urllib.request.urlopen('http://lightning-spp:8080/health').read().decode())"
```

## Monitorimi

- uptime check çdo minutë për `/healthz` dhe `/api/health`;
- alarm për 5xx, latency, restart loops dhe disk mbi 80%;
- rotacion i logjeve;
- backup ditor dhe test rikthimi mujor.

## Incidenti

1. Izolo trafikun ose aktivizo maintenance page.
2. Ruaj logjet dhe gjendjen për analizë.
3. Rikthe imazhin e fundit të njohur si të mirë.
4. Rikthe volume vetëm kur të dhënat janë dëmtuar.
5. Verifiko health checks dhe Scan → Process → Print.
6. Dokumento shkakun, ndikimin dhe masat parandaluese.
