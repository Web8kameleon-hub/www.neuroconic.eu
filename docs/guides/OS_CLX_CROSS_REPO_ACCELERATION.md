# OS-CLX Cross-Repo Acceleration (Lightweight)

Ky udhëzues sjell ide nga repos e ekipit pa e bërë këtë repo të rëndë.

## Qëllimi

- Mbajmë `www.neuroconic.eu` të lehtë dhe release-ready.
- Marrim avantazh nga repo të tjera me integrime **opsionale**.
- Zbatojmë një policy profil të tipit OS-CLX për kontroll të shpejtë.

## Integrime të rekomanduara (opsionale)

- `Web8kameleon-hub/OS-CLX`
  - Burim politikash dhe governance gates.
  - Këtu: përdor `scripts/os_clx_policy_guard.py` + `docs/governance/OS_CLX_POLICY_PROFILE.json`.

- `Web8kameleon-hub/Lightning-SPP-3.14`
  - Runtime inference/scanning backend.
  - Këtu: benchmark-et ekzistuese matin `shell/think` dhe edge-cases pa mock.

- `Web8kameleon-hub/Web8kameleon-hub-clisonix-sdk`
  - SDK contract patterns dhe client ergonomics.
  - Këtu: përdorimi i API endpoints të qarta + trace metadata consistency.

- `Web8kameleon-hub/Ultrawebthinkig-v2`, `Cwy`, `react-router-starter-template`
  - Frontend UX patterns dhe panel orchestration.
  - Këtu: adopto vetëm komponente të vogla, jo framework-migration total.

- `Web8kameleon-hub/Kloud`, `clisonixwesterneurope`
  - Cloud/deployment patterns.
  - Këtu: zbatime të lehta për CDN/cache/invalidation runbook.

## Multi-ecosystem lanes

- PyPI: `pyproject.toml` (`[project]`, `[project.scripts]`)
- npm: `packages/npm/neurosonic-shell/package.json`
- crates.io: `packages/crates/neurosonic-shell/Cargo.toml`

Parim: një source-of-truth për versionin dhe changelog, pastaj sync te paketat.

## Cloudflare readiness (light)

Kontrollohen minimumi:

- `robots.txt`
- `sitemap.xml`
- `manifest.webmanifest`

Kjo mjafton për SEO/CDN hygiene pa shtuar stack të ri.

## Si ekzekutohet policy guard

```bash
python scripts/os_clx_policy_guard.py
```

Strict mode për CI hard gate:

```bash
python scripts/os_clx_policy_guard.py --strict
```

## Rregulla praktike "pa e rënduar repo"

- Mos shto runtime të reja pa nevojë kritike.
- Shmang binary/artifacts të mëdhenj në git.
- Mbaj benchmark-et dhe policy-checks të bazuara në stdlib.
- Përdor integrime modulare, jo rewrite të plotë.
