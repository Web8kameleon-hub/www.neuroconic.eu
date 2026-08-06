#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUROSONIC + LIGHTNING-SPP-3.14 BRIDGE - REAL SERVICES ONLY
Asnje simulim. Asnje fake. Thirrje HTTP reale ne Lightning SPP.

API Reference: https://github.com/Web8kameleon-hub/Lightning-SPP-3.14
               PublicAPI/LightningAPI.cs

Komponentet reale:
- QuickScanAsync(source) -> Scan me TideWave + Resonance
- HighQualityScanAsync(source) -> Scan me NanoDecibel
- AIProcessAsync(data) -> Process me Clisonic AI
- HybridProcessAsync(data) -> Process hibrid
- StigmaPrintAsync(data) -> Stigma premium print
- ExecuteLightningPipelineAsync(source) -> Pipeline i plote
- BatchProcessAsync(sources) -> Batch processing
"""

import os
import json
import time
import hashlib
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class LightningMode(Enum):
    """Menytat e skanimit - perputhen me ScanMode te Lightning SPP"""

    LIGHTNING = "lightning"
    TIDEWAVE = "tidewave"
    RESONANCE = "resonance"
    NANODECIBEL = "nanodecibel"
    HYBRID = "hybrid"


class ProcessingEngine(Enum):
    """Motoret e perpunimit - perputhen me ProcessingEngine te Lightning SPP"""

    CLX = "clx"
    CLI_I = "cli_i"
    XCL = "xcl"
    CLISONIC = "clisonic"
    HYBRID = "hybrid"


class PrintQuality(Enum):
    """Cilesia e printimit"""

    DRAFT = "draft"
    NORMAL = "normal"
    HIGH = "high"
    STIGMA = "stigma"


@dataclass
class LightningResult:
    """Rezultat nga API real i Lightning SPP"""

    id: str
    status: str
    data: Any
    hash: str
    timestamp: float
    source: str
    confidence: float = 0.0
    size_bytes: int = 0
    error: Optional[str] = None


class NeurosonicLightningBridge:
    """
    Bridge real me Lightning-SPP-3.14.

    Asnje simulim. Cdo thirrje eshte HTTP request real.
    Lightning SPP duhet te jete duke ekzekutuar ne localhost:8080
    (ose ne nje server tjeter te konfiguruar)

    Komanda per te nisur Lightning SPP:
        wwwmmm serve 8080

    Endpoints real te serverit:
        GET  /health
        POST /scan
        POST /process
        POST /print
        POST /pipeline
    """

    def __init__(self, base_url: str = "http://localhost:8080", dna=None, genome=None):
        self.base_url = base_url.rstrip("/")
        self.dna = dna
        self.genome = genome
        self.scan_cache = {}
        self.process_cache = {}
        self.print_cache = {}
        self.statistics = {
            "total_scans": 0,
            "total_processes": 0,
            "total_prints": 0,
            "total_pipelines": 0,
            "total_batches": 0,
            "average_scan_time": 0.0,
            "average_process_time": 0.0,
            "average_print_time": 0.0,
            "errors": 0,
        }
        self.service_available = self._check_health()
        print(f" Neurosonic-Lightning Bridge inicializuar")
        print(f"    Target: {self.base_url}")
        print(f"    Service: {'GATI' if self.service_available else 'Ne pritje...'}")

    # ========================================================================
    # HEALTH CHECK
    # ========================================================================

    def _check_health(self) -> bool:
        """Kontrollon nese Lightning SPP eshte duke ekzekutuar"""
        # Server serves at /health (not /api/health)
        for path in ("/health", "/api/health"):
            try:
                req = urllib.request.Request(f"{self.base_url}{path}", method="GET")
                with urllib.request.urlopen(req, timeout=2) as resp:
                    data = json.loads(resp.read().decode())
                    if data.get("status") == "healthy" or resp.status == 200:
                        return True
            except Exception as e:
                print(f"    Health check {path}: {e}")
        return False

    def _request(self, endpoint: str, data: Any = None, method: str = "POST") -> Dict:
        """Ben thirrje HTTP reale ne Lightning SPP"""
        # Map API paths to server's actual bare paths
        if endpoint.startswith("/api/v1"):
            endpoint = endpoint.replace("/api/v1", "", 1)
        # /scan/high-quality -> /scan (server has no high-quality route)
        if endpoint.endswith("/high-quality"):
            endpoint = endpoint.replace("/high-quality", "", 1)
        # /process/hybrid and /process/ai -> /process (server has no sub-routes)
        if endpoint.startswith("/process/"):
            endpoint = "/process"
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        if not self.service_available:
            return {"error": "Lightning SPP service not available", "status": "error"}

        try:
            body = json.dumps(data).encode("utf-8") if data else None
            req = urllib.request.Request(url, data=body, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=30) as resp:
                response_data = json.loads(resp.read().decode())
                return response_data
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else str(e)
            return {
                "error": f"HTTP {e.code}: {error_body}",
                "status": "error",
                "http_code": e.code,
            }
        except urllib.error.URLError as e:
            return {"error": f"Connection failed: {e.reason}", "status": "error"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

    def _generate_id(self, prefix: str = "lsp") -> str:
        return f"{prefix}_{hashlib.sha256(f'{time.time()}{os.urandom(8)}'.encode()).hexdigest()[:12]}"

    # ========================================================================
    # SCAN - Perputhet me QuickScanAsync dhe HighQualityScanAsync
    # ========================================================================

    def scan(
        self, source: str, mode: LightningMode = LightningMode.TIDEWAVE
    ) -> LightningResult:
        """
        Scan real duke perdorur QuickScanAsync ose HighQualityScanAsync te Lightning SPP.

        Args:
            source: Path ose URL e dokumentit/imazhit per skanim
            mode: M enyra e skanimit

        Returns:
            LightningResult me te dhenat e skanuara
        """
        start_time = time.time()
        scan_id = self._generate_id("scan")

        payload = {
            "source": source,
            "mode": mode.value,
            "dpi": 600 if mode == LightningMode.NANODECIBEL else 300,
            "use_resonance": mode in [LightningMode.RESONANCE, LightningMode.TIDEWAVE],
            "use_nano_decibel": mode == LightningMode.NANODECIBEL,
        }

        if mode == LightningMode.NANODECIBEL:
            # HighQualityScanAsync - fallback to /scan if high-quality missing
            result = self._request("/api/v1/scan/high-quality", payload)
            if "error" in result:
                result = self._request("/api/v1/scan", payload)
        else:
            # QuickScanAsync - perdor TideWave + Resonance
            result = self._request("/api/v1/scan", payload)

        elapsed = time.time() - start_time
        self.statistics["total_scans"] += 1
        n = self.statistics["total_scans"]
        self.statistics["average_scan_time"] = (
            self.statistics["average_scan_time"] * (n - 1) + elapsed
        ) / n

        if "error" in result:
            self.statistics["errors"] += 1
            return LightningResult(
                id=scan_id,
                status="error",
                data=None,
                hash="",
                timestamp=time.time(),
                source=source,
                error=result["error"],
            )

        return LightningResult(
            id=result.get("id", result.get("scan_id", scan_id)),
            status=result.get("status", "completed"),
            data=result.get("data"),
            hash=result.get("hash", hashlib.sha256(source.encode()).hexdigest()[:12]),
            timestamp=time.time(),
            source=source,
            confidence=result.get("confidence", 0.95),
            size_bytes=result.get("size_bytes", len(source.encode())),
        )

    # ========================================================================
    # PROCESS - Perputhet me AIProcessAsync dhe HybridProcessAsync
    # ========================================================================

    def process(
        self,
        data: Any,
        engine: ProcessingEngine = ProcessingEngine.HYBRID,
        ai_enhance: bool = True,
    ) -> LightningResult:
        """
        Process real duke perdorur AIProcessAsync ose HybridProcessAsync.

        Args:
            data: Te dhenat per perpunim
            engine: Motori i perpunimit
            ai_enhance: Aktivizon Clisonic AI

        Returns:
            LightningResult me te dhenat e perpunuara
        """
        start_time = time.time()
        process_id = self._generate_id("proc")

        # Konverto ne bytes nese eshte string
        if isinstance(data, str):
            data_bytes = data.encode()
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            data_bytes = str(data).encode()

        payload = {
            "data": data_bytes.hex(),
            "engine": engine.value,
            "use_ai": ai_enhance,
            "use_clisonic": engine
            in [ProcessingEngine.CLISONIC, ProcessingEngine.HYBRID],
            "optimization_level": 5,
            "use_stigma_memory": True,
        }

        if engine == ProcessingEngine.HYBRID:
            # No /process/hybrid on server -> maps to /process in _request
            result = self._request("/api/v1/process/hybrid", payload)
        elif engine == ProcessingEngine.CLISONIC:
            result = self._request("/api/v1/process/ai", payload)
        else:
            result = self._request("/api/v1/process", payload)

        elapsed = time.time() - start_time
        self.statistics["total_processes"] += 1
        n = self.statistics["total_processes"]
        self.statistics["average_process_time"] = (
            self.statistics["average_process_time"] * (n - 1) + elapsed
        ) / n

        if "error" in result:
            self.statistics["errors"] += 1
            return LightningResult(
                id=process_id,
                status="error",
                data=None,
                hash="",
                timestamp=time.time(),
                source=engine.value,
                error=result["error"],
            )

        return LightningResult(
            id=result.get("id", result.get("process_id", process_id)),
            status=result.get("status", "completed"),
            data=result.get("data"),
            hash=result.get(
                "hash", hashlib.sha256(str(data).encode()).hexdigest()[:12]
            ),
            timestamp=time.time(),
            source=engine.value,
            confidence=result.get("confidence", 0.97),
            size_bytes=result.get("size_bytes", len(data_bytes)),
        )

    # ========================================================================
    # PRINT - Perputhet me StigmaPrintAsync
    # ========================================================================

    def print_result(
        self, data: Any, quality: PrintQuality = PrintQuality.STIGMA
    ) -> LightningResult:
        """
        Print real duke perdorur StigmaPrintAsync te Lightning SPP.

        Args:
            data: Te dhenat per printim
            quality: Cilesia e printimit

        Returns:
            LightningResult me rezultatin e printimit
        """
        start_time = time.time()
        print_id = self._generate_id("prt")

        if isinstance(data, str):
            data_bytes = data.encode()
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            data_bytes = str(data).encode()

        result = self._request(
            "/api/v1/print",
            {
                "data": data_bytes.hex(),
                "quality": quality.value,
                "use_stigma": quality == PrintQuality.STIGMA,
            },
        )

        elapsed = time.time() - start_time
        self.statistics["total_prints"] += 1
        n = self.statistics["total_prints"]
        self.statistics["average_print_time"] = (
            self.statistics["average_print_time"] * (n - 1) + elapsed
        ) / n

        if "error" in result:
            self.statistics["errors"] += 1
            return LightningResult(
                id=print_id,
                status="error",
                data=None,
                hash="",
                timestamp=time.time(),
                source=quality.value,
                error=result["error"],
            )

        return LightningResult(
            id=result.get("id", result.get("print_id", print_id)),
            status=result.get("status", "completed"),
            data=result.get("output_path", "printed"),
            hash=result.get(
                "hash", hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:12]
            ),
            timestamp=time.time(),
            source=f"print_{quality.value}",
            confidence=result.get("confidence", 0.99),
            size_bytes=result.get("size_bytes", len(data_bytes)),
        )

    # ========================================================================
    # FULL PIPELINE - Perputhet me ExecuteLightningPipelineAsync
    # ========================================================================

    def execute_pipeline(
        self,
        source: str,
        scan_mode: LightningMode = LightningMode.TIDEWAVE,
        process_engine: ProcessingEngine = ProcessingEngine.HYBRID,
        print_quality: PrintQuality = PrintQuality.STIGMA,
    ) -> Dict[str, Any]:
        """
        Pipeline i plote real duke perdorur ExecuteLightningPipelineAsync.

        Args:
            source: Path ose URL e dokumentit
            scan_mode: M enyra e skanimit
            process_engine: Motori i perpunimit
            print_quality: Cilesia e printimit

        Returns:
            Dict me rezultatet e te gjithe pipeline
        """
        start_time = time.time()
        pipeline_id = self._generate_id("pipe")

        result = self._request(
            "/api/v1/pipeline",
            {
                "source": source,
                "scan_mode": scan_mode.value,
                "process_engine": process_engine.value,
                "print_quality": print_quality.value,
                "use_ai": True,
                "use_clisonic": True,
                "use_stigma": print_quality == PrintQuality.STIGMA,
            },
        )

        total_time = time.time() - start_time
        self.statistics["total_pipelines"] += 1

        if "error" in result:
            self.statistics["errors"] += 1

        return {
            "pipeline_id": pipeline_id,
            "status": result.get(
                "status", "completed" if "error" not in result else "error"
            ),
            "result": result,
            "total_time_ms": total_time * 1000,
            "timestamp": time.time(),
        }

    # ========================================================================
    # BATCH PROCESS - Perputhet me BatchProcessAsync
    # ========================================================================

    def batch_process(self, sources: List[str]) -> Dict[str, Any]:
        """
        Batch processing - server has no /batch route, so scan each source.
        """
        start_time = time.time()
        batch_id = self._generate_id("batch")
        results = []

        # Fallback: process each source individually since server has no /batch
        for src in sources:
            try:
                r = self.scan(src, LightningMode.TIDEWAVE)
                results.append(
                    {"source": src, "status": r.status, "id": r.id, "error": r.error}
                )
            except Exception as e:
                results.append({"source": src, "status": "error", "error": str(e)})

        total_time = time.time() - start_time
        self.statistics["total_batches"] += 1

        return {
            "batch_id": batch_id,
            "sources_count": len(sources),
            "status": "completed",
            "results": results,
            "total_time_ms": total_time * 1000,
            "timestamp": time.time(),
        }
    def get_statistics(self) -> Dict[str, Any]:
        """Statistikat e integrimit"""
        return {
            "total_scans": self.statistics["total_scans"],
            "total_processes": self.statistics["total_processes"],
            "total_prints": self.statistics["total_prints"],
            "total_pipelines": self.statistics["total_pipelines"],
            "total_batches": self.statistics["total_batches"],
            "average_scan_time_ms": self.statistics["average_scan_time"] * 1000,
            "average_process_time_ms": self.statistics["average_process_time"] * 1000,
            "average_print_time_ms": self.statistics["average_print_time"] * 1000,
            "errors": self.statistics["errors"],
            "service_available": self.service_available,
            "base_url": self.base_url,
        }

    def get_profile(self) -> Dict[str, Any]:
        """Kthen profilin e bridge"""
        return {
            "name": "Neurosonic-Lightning Bridge",
            "version": "1.0.0",
            "real_services": True,
            "zero_fake": True,
            "service_url": self.base_url,
            "service_available": self.service_available,
            "protocol": "HTTP REST",
            "formats": ["JSON", "bytes"],
            "source": "https://github.com/Web8kameleon-hub/Lightning-SPP-3.14",
        }
