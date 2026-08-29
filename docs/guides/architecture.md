# Neurosonic Architecture Overview

> **Constitutional grounding:** G004, G005, G006, G007; architecture docs.

## At a glance

Neurosonic Trinity+ASI is a **modular AI operating environment** built with zero
external dependencies. Its architecture is defined by an immutable **DNA**
(`neurosonic_dna.py`), an extensible **Genome** (`neurosonic_genome.py`), and
companion modules for compatibility, evolution, security, and the Lightning SPP
bridge.

## Core design laws

The constitution (G001-G010) defines the boundaries of the architecture:

- **G004 - Internal Infrastructure Law:** everything critical is built internally.
- **G005 - Modular Law:** every component is a replaceable module.
- **G006 - Distributed Law:** no central brain; every device can be a cognitive node.
- **G007 - Security Law:** Zero Trust; encryption everywhere.

## Main components

| Component | Role |
|-----------|------|
| CLX Kernel | Core runtime and resource scheduler. |
| HVO Memory | Six memory types (see [HVO Memory](hvo-memory.md)). |
| Internal Auth | Internal authentication, no external OAuth. |
| NodeDB Fluid | Adaptive database. |
| Thinking Pipeline | 11-step reasoning pipeline. |
| Agent Society | Collaborative agents (Research, Country, Security, Protocol). |
| SSE Streaming | Server-sent-event streaming. |
| Tide Engine | Cyclical "tide" processing engine. |
| Security Engine | Zero Trust, DDoS protection, encryption. |
| Internal Economy | Wallet, licensing, billing. |
| Audit Logger | Immutable audit logs. |
| NO FAKE Police | CI/CD enforcement of the truth policy. |

## Security model

The security rules (SR001-SR008) enforce **Zero Trust**: verify everything,
encrypt at rest and in transit, keep immutable audit logs, validate AI actions,
preserve privacy by design, and guarantee **Human Override (SR007)** plus
**Emergency Stop (SR008)** - humans always retain final authority.

## Running the system

```bash
# Clone the repository
git clone https://github.com/LedjanAhmati/www.neurosonic.eu
cd www.neurosonic.eu

# Run - zero installs required
python neurosonic.py

# Run the test suite
python test_architecture.py

# Enforce the NO FAKE policy in CI
python neurosonic_no_fake_police.py --ci
```

## Related

- [Zero Fake](zero-fake.md)
- [HVO Memory](hvo-memory.md)
- [Architecture documentation](../Architecture.md)
- [Constitution](../Constitution.md)

