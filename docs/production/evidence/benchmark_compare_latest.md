# Comparative Benchmark Evidence

- Baseline: `logs/benchmarks/first-benchmark-20260902-205726.json`
- Candidate: `logs/benchmarks/first-benchmark-20260902-205731.json`
- Shared scenarios: `7`
- Overall pass-rate delta: `0.0`

| Scenario | Δ p95 (ms) | Δ p95 (%) | Δ Throughput (rps) | Δ Throughput (%) | Δ Pass Rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| plugin_attach_private_network_edge | 0.351 | 9.15 | -20.707 | -6.8 | 0.0 |
| plugin_attach_sensitive_metadata_edge | 5.879 | 154.02 | -129.585 | -42.59 | 0.0 |
| plugin_attach_success_baseline | 0.448 | 8.58 | -2.026 | -0.95 | 0.0 |
| shell_think_echo_edge | 0.019 | 0.42 | 4.381 | 1.69 | 0.0 |
| shell_think_empty_prompt_edge | -0.287 | -6.77 | 27.531 | 9.88 | 0.0 |
| shell_think_long_prompt_tuning | 0.407 | 9.57 | -8.484 | -3.18 | 0.0 |
| shell_think_reasoning_success | -0.377 | -8.45 | 17.209 | 6.56 | 0.0 |
