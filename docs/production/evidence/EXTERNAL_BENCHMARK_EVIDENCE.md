# External Benchmark Evidence

## Scope

This document records external benchmark references and how they are mapped to local evidence artifacts.

## Referenced External Sources

- **TechEmpower Web Framework Benchmarks**: `https://www.techempower.com/benchmarks/`
  - Public benchmark rounds and test categories for HTTP/database workloads.
  - Round-based publication with environment context.
- **TechEmpower FrameworkBenchmarks repo**: `https://github.com/TechEmpower/FrameworkBenchmarks`
  - Open benchmark harness and reproducibility scripts.
  - Repository is archived/read-only in 2026 (important for maintenance expectations).
- **Python Performance Benchmark Suite**: `https://pyperformance.readthedocs.io/`
  - Authoritative Python benchmark suite with real-world focus and stability guidance.
- **OpenTelemetry Trace API**: `https://opentelemetry.io/docs/specs/otel/trace/api/`
  - Defines trace/span semantics used for uniform tracing baseline.

## Local Evidence Mapping

- Local benchmark artifacts:
  - `logs/benchmarks/live-benchmark-*.json`
  - `docs/production/evidence/benchmark_compare_latest.json`
  - `docs/production/evidence/benchmark_compare_latest.md`
- Observability evidence:
  - `docs/production/evidence/latency_trend.json`
  - `docs/production/evidence/availability_trend.json`
  - `docs/production/evidence/slo_snapshot_latest.json`

## Credibility Boundary

- This repository **does not claim external rank parity** unless tests are run with the same harness and comparable hardware/network conditions.
- Current evidence demonstrates, after live runs are collected:
  - local HTTP benchmark measurements,
  - explicit methodology references,
  - and transparent limitations.
