# Zero Fake AI - The Neurosonic Approach

> **Constitutional grounding:** G001 Truth Law, QR001-QR005 Quality Rules, G008 Intelligence Law.

## What is "Zero Fake"?

Zero Fake is Neurosonic's commitment that **no fabricated knowledge** is ever
produced or presented as fact. It is encoded in the top law of the constitution:

> **G001 - Truth Law:** "No Fake. No fabricated knowledge."

## How Neurosonic enforces truth

Truth is not a policy document in Neurosonic - it is *architecture*. These are the
mechanisms defined in the source (`neurosonic_dna.py`) that enforce the
constitution:

| Rule | ID | Meaning |
|------|----|---------|
| Zero Fake | QR001 | No fabricated information is produced. |
| Zero Hallucination | QR002 | All outputs are verified before delivery. |
| Zero Noise | QR003 | Only clean, relevant data is used. |
| Source Verification | QR004 | Every fact has a verifiable source. |
| Hash Verification | QR005 | Every response carries a hash for integrity. |

These sit on top of the **Intelligence Law (G008)** - *"Every intelligence passes
through validation"* - meaning results are checked before they are ever exposed.

## The validation pipeline

Neurosonic's Thinking Pipeline routes every request through 11 steps:
`Scanner → Intent → Planner → Memory → Knowledge → Reasoning → Validator →
Response → Learning`.

The critical gate is the **Validator** step: it rejects anything that cannot be
backed by a source, and only then does a response reach the **Response** step.

## Source and hash verification

Per the constitution (Shtylla 2 / Pillar 2), every response must carry:

1. A **source URL** (verifiable reference).
2. A **SHA-256 hash** (integrity of the content).
3. A **timestamp** (versioning / provenance).

If three independent sources cannot confirm a statement, the system's rule is to
say **"I don't know"** rather than fabricate an answer.

## Why this matters

In an era where many AI systems produce hallucinations, Neurosonic treats truth
as a first-class, enforceable property of the system - not an aspiration. This is
both a security property and a core differentiator.

## Related

- [Architecture](architecture.md)
- [HVO Memory](hvo-memory.md)
- [Constitution](../Constitution.md)
- [NO FAKE Policy](../../NO_FAKE_POLICY.md)

