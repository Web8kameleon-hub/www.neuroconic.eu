#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC BACKEND API - FastAPI
Ekspozon modulet Neurosonic si REST API per frontend-in.
"""

import sys
import os
import time
import json
import hashlib
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Shto parent directory per import - absolute path
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _project_root)
os.chdir(_project_root)

from neurosonic_dna import NeurosonicDNA
from neurosonic_genome import NeurosonicGenome, GenomePackage
from neurosonic_compatibility import NeurosonicCompatibilityMatrix
from neurosonic_evolution import NeurosonicEvolutionEngine
from neurosonic_lightning_bridge import (
    NeurosonicLightningBridge,
    LightningMode,
    ProcessingEngine,
    PrintQuality,
)

app = FastAPI(
    title="Neurosonic Trinity+ASI API",
    description="Backend API per Neurosonic - DNA, Genome, Compatibility, Evolution, Lightning SPP",
    version="1.0.0",
)

# CORS - lejo frontend nga cdokush burim
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializo modulet Neurosonic
dna = NeurosonicDNA()
genome = NeurosonicGenome()
matrix = NeurosonicCompatibilityMatrix(dna, genome)
evolution = NeurosonicEvolutionEngine(dna, genome)
bridge = NeurosonicLightningBridge(dna=dna, genome=genome)

print("=" * 60)
print("  NEUROSONIC BACKEND API GATI!")
print("  DNA | GENOME | COMPATIBILITY | EVOLUTION | LIGHTNING")
print("=" * 60)


# ========================================================================
# Pydantic Models
# ========================================================================


class ModuleVerifyRequest(BaseModel):
    module_id: str
    config: Dict[str, Any]


class EvolutionProposeRequest(BaseModel):
    description: str
    category: str = "governance"
    impact_level: str = "medium"


class ScanRequest(BaseModel):
    source: str
    mode: str = "tidewave"


class ProcessRequest(BaseModel):
    data: str
    engine: str = "hybrid"
    ai_enhance: bool = True


class PrintRequest(BaseModel):
    data: str
    quality: str = "stigma"


class PipelineRequest(BaseModel):
    source: str
    scan_mode: str = "tidewave"
    process_engine: str = "hybrid"
    print_quality: str = "stigma"


class BatchRequest(BaseModel):
    sources: List[str]


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
        "docs": "/docs",
    }


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "dna_integrity": dna._hash == dna._compute_dna_hash(),
        "genome_packages": len(genome.packages),
        "lightning_service": bridge.service_available,
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
    return {
        "module_id": result.module_id,
        "compatible": result.compatible,
        "score": result.score,
        "violations": result.violations,
        "checks": result.checks,
        "hash": result.hash,
        "timestamp": result.timestamp,
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
    try:
        mode = LightningMode(req.mode)
    except ValueError:
        mode = LightningMode.TIDEWAVE
    result = bridge.scan(req.source, mode)
    return {
        "id": result.id,
        "status": result.status,
        "data": result.data,
        "hash": result.hash,
        "confidence": result.confidence,
        "error": result.error,
        "timestamp": result.timestamp,
    }


@app.post("/api/lightning/process")
async def lightning_process(req: ProcessRequest):
    try:
        engine = ProcessingEngine(req.engine)
    except ValueError:
        engine = ProcessingEngine.HYBRID
    result = bridge.process(req.data, engine, req.ai_enhance)
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
    try:
        quality = PrintQuality(req.quality)
    except ValueError:
        quality = PrintQuality.STIGMA
    result = bridge.print_result(req.data, quality)
    return {
        "id": result.id,
        "status": result.status,
        "data": result.data,
        "hash": result.hash,
        "confidence": result.confidence,
        "error": result.error,
        "timestamp": result.timestamp,
    }


@app.post("/api/lightning/pipeline")
async def lightning_pipeline(req: PipelineRequest):
    try:
        scan_mode = LightningMode(req.scan_mode)
    except ValueError:
        scan_mode = LightningMode.TIDEWAVE
    try:
        proc_engine = ProcessingEngine(req.process_engine)
    except ValueError:
        proc_engine = ProcessingEngine.HYBRID
    try:
        print_q = PrintQuality(req.print_quality)
    except ValueError:
        print_q = PrintQuality.STIGMA
    result = bridge.execute_pipeline(req.source, scan_mode, proc_engine, print_q)
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


# ========================================================================
# Main
# ========================================================================

if __name__ == "__main__":
    import uvicorn

    print("\n🔌 Neurosonic Backend API duke u nisur...")
    print("   http://localhost:8000")
    print("   http://localhost:8000/docs (Swagger UI)")
    print("   http://localhost:8000/redoc (ReDoc)\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
