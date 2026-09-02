#!/usr/bin/env python3
# ruff: noqa: I001
"""
NEUROSONIC BACKEND API - FastAPI
Ekspozon modulet Neurosonic si REST API per frontend-in.
"""

import hashlib
import json
import os
import sys
import time
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Shto parent directory per import - absolute path
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _project_root)
os.chdir(_project_root)

from neurosonic_compatibility import NeurosonicCompatibilityMatrix
from neurosonic_data_intelligence import (
    PlirisDatenFilter,
    SeltenDatenAnalyzer,
    SelfLearningCycleManager,
)
from neurosonic_dna import NeurosonicDNA
from neurosonic_evolution import NeurosonicEvolutionEngine
from neurosonic_genome import NeurosonicGenome
from neurosonic_lightning_bridge import (
    LightningMode,
    NeurosonicLightningBridge,
    PrintQuality,
    ProcessingEngine,
)

app = FastAPI(
    title="Neurosonic Trinity+ASI API",
    description="Backend API per Neurosonic - DNA, Genome, Compatibility, Evolution, Lightning SPP",
    version="1.0.0",
)

_cors_origins = [
    origin.strip()
    for origin in os.environ.get("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializo modulet Neurosonic
dna = NeurosonicDNA()
genome = NeurosonicGenome()
matrix = NeurosonicCompatibilityMatrix(dna, genome)
evolution = NeurosonicEvolutionEngine(dna, genome)
bridge = NeurosonicLightningBridge(dna=dna, genome=genome)
selten_analyzer = SeltenDatenAnalyzer()
pliris_filter = PlirisDatenFilter()
self_learning = SelfLearningCycleManager()

print("=" * 60)
print("  NEUROSONIC BACKEND API GATI!")
print("  DNA | GENOME | COMPATIBILITY | EVOLUTION | LIGHTNING")
print("=" * 60)


# ========================================================================
# Pydantic Models
# ========================================================================


class ModuleVerifyRequest(BaseModel):
    module_id: str
    config: dict[str, Any]


class EvolutionProposeRequest(BaseModel):
    description: str
    category: str = "governance"
    impact_level: str = "medium"


class ScanRequest(BaseModel):
    source: str
    mode: LightningMode = LightningMode.TIDEWAVE


class ProcessRequest(BaseModel):
    data: str
    engine: ProcessingEngine = ProcessingEngine.HYBRID
    ai_enhance: bool = True


class PrintRequest(BaseModel):
    data: str
    quality: PrintQuality = PrintQuality.STIGMA


class PipelineRequest(BaseModel):
    source: str
    scan_mode: LightningMode = LightningMode.TIDEWAVE
    process_engine: ProcessingEngine = ProcessingEngine.HYBRID
    print_quality: PrintQuality = PrintQuality.STIGMA


class BatchRequest(BaseModel):
    sources: list[str]


class ShellThinkRequest(BaseModel):
    prompt: str
    engine: ProcessingEngine = ProcessingEngine.HYBRID


class SeltenDatenRequest(BaseModel):
    records: list[dict[str, Any]]
    key_fields: list[str] | None = None
    rarity_threshold: float = 0.1
    min_occurrences: int = 1


class PlirisDatenRequest(BaseModel):
    records: list[dict[str, Any]]


class SelfLearningCycleRequest(BaseModel):
    goal: str
    context: dict[str, Any] = {}
    engine: ProcessingEngine = ProcessingEngine.HYBRID
    ai_enhance: bool = True


# ========================================================================
# Endpoints
# ========================================================================


@app.get("/")
async def root():
    return {
        "name": "Neurosonic Trinity+ASI",
        "version": "1.0.0",
        "status": "online",
        "modules": ["dna", "genome", "compatibility", "evolution", "lightning"],
        "ui": {
            "dashboard": "/dashboard",
            "dashboard_file": "/neurosonic_dashboard.html",
            "dna_ui": "/dna-ui",
            "dna_ui_file": "/neurosonic_dna_ui.html",
            "frontend_entry": "/index.html",
        },
        "docs": "/docs",
    }


@app.get("/neurosonic_dashboard.html", include_in_schema=False)
async def dashboard():
    """Shërben dashboard-in nga i njëjti origin me API-n."""
    return FileResponse(os.path.join(_project_root, "neurosonic_dashboard.html"))


@app.get("/dashboard", include_in_schema=False)
async def dashboard_alias():
    """Alias i qartë për dashboard-in e API/ops."""
    return FileResponse(os.path.join(_project_root, "neurosonic_dashboard.html"))


@app.get("/index.html", include_in_schema=False)
async def frontend_index():
    """Shërben hyrjen historike të frontend-it."""
    return FileResponse(os.path.join(_project_root, "index.html"))


@app.get("/dna-ui", include_in_schema=False)
async def dna_ui():
    """UI e dedikuar për ADN-në."""
    return FileResponse(os.path.join(_project_root, "neurosonic_dna_ui.html"))


@app.get("/neurosonic_dna_ui.html", include_in_schema=False)
async def dna_ui_file():
    """Alias historik për UI e ADN-së."""
    return FileResponse(os.path.join(_project_root, "neurosonic_dna_ui.html"))


@app.get("/dna-dashboard", include_in_schema=False)
async def dna_dashboard_alias():
    """Alias i qartë për dashboard-in DNA UI."""
    return FileResponse(os.path.join(_project_root, "neurosonic_dna_ui.html"))


@app.get("/api/health")
async def health():
    lightning_service = bridge._check_health()
    bridge.service_available = lightning_service
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "dna_integrity": dna._hash == dna._compute_dna_hash(),
        "genome_packages": len(genome.packages),
        "lightning_service": lightning_service,
        "api_version": "1.0.0",
    }


@app.get("/api/dna")
async def get_dna():
    return {
        "name": dna.name,
        "immutable": dna.immutable,
        "hash": dna._hash,
        "stats": dna.get_stats(),
        "rules": {
            "constitution": [
                {"id": k, "name": v["name"], "description": v["text"]}
                for k, v in dna.CONSTITUTION.items()
            ],
            "security": [
                {"id": k, "name": v.split(" - ")[0], "description": v}
                for k, v in dna.SECURITY_RULES.items()
            ],
            "data": [
                {"id": k, "name": v.split(" - ")[0], "description": v}
                for k, v in dna.DATA_RULES.items()
            ],
            "api": [
                {"id": k, "name": v.split(" - ")[0], "description": v}
                for k, v in dna.API_RULES.items()
            ],
            "memory": [
                {"id": k, "name": v.split(" - ")[0], "description": v}
                for k, v in dna.MEMORY_RULES.items()
            ],
            "governance": [
                {"id": k, "name": v.split(" - ")[0], "description": v}
                for k, v in dna.GOVERNANCE_RULES.items()
            ],
            "quality": [
                {"id": k, "name": v.split(" - ")[0], "description": v}
                for k, v in dna.QUALITY_RULES.items()
            ],
            "core_values": [
                {"id": k, "name": k.upper(), "description": v}
                for k, v in dna.CORE_VALUES.items()
            ],
        },
    }


@app.get("/api/genome")
async def get_genome():
    packages = genome.list_packages()
    categories = genome.get_packages_by_category()
    cat_map = {}
    for cat, pkgs in categories.items():
        for p in pkgs:
            cat_map[p["id"]] = cat
    for pkg in packages:
        pkg["category"] = cat_map.get(pkg["id"], "other")
    return {
        "total": len(packages),
        "categories": {
            cat: [p["id"] for p in pkgs] for cat, pkgs in categories.items()
        },
        "packages": packages,
        "stats": genome.get_stats(),
    }


@app.post("/api/compatibility/verify")
async def verify_compatibility(req: ModuleVerifyRequest):
    result = matrix.verify_module(req.module_id, req.config)
    report = matrix.generate_report(result)
    total_checks = len(result.checks) if result.checks else 0
    passed_checks = sum(1 for passed in result.checks.values() if passed)
    score = (passed_checks / total_checks) * 100 if total_checks else 0.0
    payload_hash = hashlib.sha256(
        json.dumps(
            {
                "module_id": result.module_id,
                "module_name": result.module_name,
                "compatible": result.compatible,
                "checks": result.checks,
                "violations": result.violations,
            },
            sort_keys=True,
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()
    timestamp = time.time()
    return {
        "module_id": result.module_id,
        "compatible": result.compatible,
        "score": score,
        "violations": result.violations,
        "checks": result.checks,
        "hash": payload_hash,
        "timestamp": timestamp,
        "report": report,
    }


@app.get("/api/evolution/analyze")
async def analyze_architecture():
    analysis = evolution.analyze_architecture()
    return analysis


@app.post("/api/evolution/propose")
async def propose_change(req: EvolutionProposeRequest):
    proposal = evolution.propose_new_rule(
        description=req.description,
        category=req.category,
        impact_level=req.impact_level,
    )
    return proposal


@app.get("/api/evolution/proposals")
async def get_proposals():
    return {
        "proposals": evolution.get_proposals_summary(),
        "stats": evolution.get_stats(),
    }


@app.post("/api/lightning/scan")
async def lightning_scan(req: ScanRequest):
    result = bridge.scan(req.source, req.mode)
    return {
        "id": result.id,
        "status": result.status,
        "data": result.data,
        "source": result.source,
        "hash": result.hash,
        "confidence": result.confidence,
        "error": result.error,
        "timestamp": result.timestamp,
    }


@app.post("/api/lightning/process")
async def lightning_process(req: ProcessRequest):
    result = bridge.process(req.data, req.engine, req.ai_enhance)
    return {
        "id": result.id,
        "status": result.status,
        "data": result.data,
        "hash": result.hash,
        "confidence": result.confidence,
        "error": result.error,
        "timestamp": result.timestamp,
    }


@app.post("/api/lightning/print")
async def lightning_print(req: PrintRequest):
    result = bridge.print_result(req.data, req.quality)
    return {
        "id": result.id,
        "status": result.status,
        "data": result.data,
        "source": result.source,
        "hash": result.hash,
        "confidence": result.confidence,
        "error": result.error,
        "timestamp": result.timestamp,
    }


@app.post("/api/lightning/pipeline")
async def lightning_pipeline(req: PipelineRequest):
    result = bridge.execute_pipeline(
        req.source, req.scan_mode, req.process_engine, req.print_quality
    )
    return result


@app.post("/api/lightning/batch")
async def lightning_batch(req: BatchRequest):
    result = bridge.batch_process(req.sources)
    return result


@app.get("/api/lightning/stats")
async def lightning_stats():
    return bridge.get_statistics()


@app.get("/api/lightning/profile")
async def lightning_profile():
    return bridge.get_profile()


@app.post("/api/data/selten/discover")
async def selten_daten_discover(req: SeltenDatenRequest):
    return selten_analyzer.detect_rare(
        records=req.records,
        key_fields=req.key_fields,
        rarity_threshold=req.rarity_threshold,
        min_occurrences=req.min_occurrences,
    )


@app.post("/api/data/pliris/filter")
async def pliris_daten_filter(req: PlirisDatenRequest):
    return pliris_filter.filter_protocol_free(req.records)


@app.post("/api/self-learning/cycle")
async def self_learning_cycle(req: SelfLearningCycleRequest):
    def _engine_callback(prompt: str, engine_name: str) -> dict[str, Any]:
        engine = ProcessingEngine(engine_name)
        result = bridge.process(prompt, engine, req.ai_enhance)
        if result.error or result.status == "error":
            return {
                "success": False,
                "status": "service_unavailable",
                "error": result.error or "Processing failed",
                "engine": engine.value,
                "timestamp": time.time(),
            }

        response_text = ""
        if isinstance(result.data, (dict, list)):
            response_text = json.dumps(result.data, ensure_ascii=False)
        elif result.data is None:
            response_text = ""
        else:
            response_text = str(result.data)

        return {
            "success": True,
            "status": result.status,
            "response": response_text,
            "hash": result.hash,
            "confidence": result.confidence,
            "engine": engine.value,
            "timestamp": time.time(),
        }

    return self_learning.create_cycle(
        goal=req.goal,
        context=req.context,
        llm_engine=req.engine.value,
        engine_callback=_engine_callback,
    )


@app.get("/api/self-learning/cycles")
async def self_learning_cycles(limit: int = 20):
    return self_learning.get_cycles(limit=limit)


@app.post("/api/shell/think")
async def shell_think(req: ShellThinkRequest):
    started_at = time.time()
    prompt = req.prompt.strip()
    if not prompt:
        return {
            "success": False,
            "status": "error",
            "error": "Prompt is empty",
            "timestamp": time.time(),
        }

    result = bridge.process(prompt, req.engine, True)
    elapsed_ms = (time.time() - started_at) * 1000

    if result.error or result.status == "error":
        return {
            "success": False,
            "status": "service_unavailable",
            "error": result.error or "Processing failed",
            "engine": req.engine.value,
            "latency_ms": elapsed_ms,
            "timestamp": time.time(),
            "verified": False,
            "sources": [bridge.base_url],
        }

    output_text = ""
    if isinstance(result.data, (dict, list)):
        output_text = json.dumps(result.data, ensure_ascii=False)
    elif result.data is None:
        output_text = ""
    else:
        output_text = str(result.data)
        if output_text and len(output_text) % 2 == 0:
            try:
                output_text = bytes.fromhex(output_text).decode("utf-8")
            except ValueError:
                pass

    return {
        "success": True,
        "status": result.status,
        "response": output_text,
        "hash": result.hash,
        "confidence": result.confidence,
        "engine": req.engine.value,
        "latency_ms": elapsed_ms,
        "timestamp": time.time(),
        "verified": True,
        "sources": [bridge.base_url, "dna:" + dna._hash],
    }


# ========================================================================
# Main
# ========================================================================

if __name__ == "__main__":
    import uvicorn

    print("\n🔌 Neurosonic Backend API duke u nisur...")
    host = os.environ.get("NEUROSONIC_HOST", "127.0.0.1")
    port = int(os.environ.get("NEUROSONIC_PORT", "8000"))
    print(f"   Backend listening on {host}:{port}\n")
    uvicorn.run(app, host=host, port=port, reload=False)
