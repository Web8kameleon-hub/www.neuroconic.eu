from __future__ import annotations

from scripts import benchmark_edge_cases as edge


def test_edge_verifiers_follow_api_contracts() -> None:
    assert edge._prompt_empty_error(200, {"success": False, "error": "Prompt is empty"})
    assert edge._requires_liability_ack(
        200,
        {"success": False, "error": "liability_ack must be true"},
    )
    assert edge._rejects_private_address(
        200,
        {"success": False, "error": "private or local network is blocked"},
    )
    assert edge._rejects_sensitive_metadata(
        200,
        {"success": False, "error": "contains sensitive key"},
    )


def test_run_scenario_computes_pass_rate(monkeypatch) -> None:
    scenario = edge.EdgeScenario(
        name="contract-check",
        endpoint="/api/shell/think",
        method="POST",
        payload={"prompt": "hello"},
        verifier=lambda status, body: status == 200 and body.get("ok") is True,
    )

    def fake_request(base_url: str, received_scenario: edge.EdgeScenario, timeout: float):
        assert base_url == "http://127.0.0.1:8000"
        assert received_scenario.name == "contract-check"
        assert timeout == 5.0
        return 200, {"ok": True, "status": "healthy"}

    monkeypatch.setattr(edge, "_request", fake_request)

    report = edge._run_scenario(
        "http://127.0.0.1:8000",
        scenario,
        iterations=4,
        warmup=1,
        timeout=5.0,
    )

    assert report["name"] == "contract-check"
    assert report["pass_rate"] == 1.0
    assert report["iterations"] == 4
    assert report["warmup"] == 1
    assert report["latency_ms"]["p95"] >= 0.0
    assert report["throughput_rps"] >= 0.0
    assert report["samples"][0]["pass"] is True


def test_to_markdown_renders_expected_columns() -> None:
    markdown = edge._to_markdown(
        {
            "base_url": "http://127.0.0.1:8000",
            "iterations": 3,
            "warmup": 1,
            "totals": {"overall_pass_rate": 1.0},
            "results": [
                {
                    "name": "shell_empty_prompt_edge",
                    "pass_rate": 1.0,
                    "latency_ms": {"p95": 4.2},
                    "throughput_rps": 123.45,
                }
            ],
        }
    )

    assert "# Edge Case Benchmark Report" in markdown
    assert "| Scenario | Pass Rate | P95 (ms) | Throughput (rps) |" in markdown
    assert "shell_empty_prompt_edge" in markdown


def test_scenarios_inventory_covers_declared_edge_contracts() -> None:
    scenarios = edge._scenarios(2048)

    scenario_names = {item.name for item in scenarios}
    assert len(scenarios) == 6
    assert "shell_empty_prompt_edge" in scenario_names
    assert "shell_whitespace_prompt_edge" in scenario_names
    assert "shell_long_prompt_edge" in scenario_names
    assert "plugin_attach_missing_liability_ack_edge" in scenario_names
    assert "plugin_attach_private_network_edge" in scenario_names
    assert "plugin_attach_sensitive_metadata_edge" in scenario_names

    long_prompt_scenario = next(
        item for item in scenarios if item.name == "shell_long_prompt_edge"
    )
    assert long_prompt_scenario.payload is not None
    assert len(long_prompt_scenario.payload["prompt"]) == 2048


def test_run_scenario_reports_failure_pass_rate(monkeypatch) -> None:
    scenario = edge.EdgeScenario(
        name="failure-check",
        endpoint="/api/shell/think",
        method="POST",
        payload={"prompt": "hello"},
        verifier=lambda status, body: status == 200 and body.get("ok") is True,
    )

    def fake_request(base_url: str, received_scenario: edge.EdgeScenario, timeout: float):
        assert base_url == "http://127.0.0.1:8000"
        assert received_scenario.name == "failure-check"
        assert timeout == 5.0
        return 200, {"ok": False, "status": "healthy", "error": "mismatch"}

    monkeypatch.setattr(edge, "_request", fake_request)

    report = edge._run_scenario(
        "http://127.0.0.1:8000",
        scenario,
        iterations=3,
        warmup=0,
        timeout=5.0,
    )

    assert report["pass_rate"] == 0.0
    assert len(report["samples"]) == 3
    assert report["samples"][0]["pass"] is False
    assert report["samples"][0]["error"] == "mismatch"


def test_percentile_interpolation_contract() -> None:
    assert edge._percentile([10.0], 0.95) == 10.0
    assert edge._percentile([10.0, 20.0, 30.0, 40.0], 0.50) == 25.0
