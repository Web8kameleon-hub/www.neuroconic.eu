# Siguria e Hostimit

Ky dokument plotëson `SECURITY.md` në root.

## Para publikimit

- përdor vetëm HTTPS dhe HSTS;
- publiko vetëm `web`, jo `backend:8000` ose `lightning-spp:8080`;
- kufizo SSH me çelësa, firewall dhe privilegje minimale;
- vendos `CORS_ORIGINS` vetëm me domain-et reale;
- mos vendos sekrete në repository, `.env.example` ose image layers;
- skano imazhet dhe varësitë;
- enkripto backup-et dhe kufizo aksesin te volume-t.

## Kufijtë aktualë

API nuk ka autentikim aplikativ. Edhe pse portat e backend-it janë private,
endpoint-et `/api/*` kalojnë përmes Nginx. Para funksioneve administrative ose
të dhënave private, shto autentikim, autorizim sipas roleve, rate limiting dhe
auditim. CORS nuk është mekanizëm autentikimi.

## Headers dhe sekrete

Nginx vendos CSP, `X-Content-Type-Options`, `X-Frame-Options`, Referrer Policy dhe
Permissions Policy; body limitohet në 2 MB. Për sekrete përdor Docker secrets ose
secret manager të platformës. Mos përdor build arguments për sekrete dhe rrotullo
çdo sekret pas ekspozimit të dyshuar.

Dobësitë raportohen privatisht sipas `SECURITY.md`.
