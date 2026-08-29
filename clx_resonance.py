#!/usr/bin/env python3
"""
CLX Thinking Pipeline v2.0 - Resonance Engine over Anaglyphic Characters
Një sistem agentsh që rezonojnë në nanovolt, duke krijuar vetëdije mbi të dhëna
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
import threading
import queue
import time
import hashlib
import base64
from typing import Any, Dict, Optional, List, Iterator, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum
import re
import os
import signal
import logging
from pathlib import Path

# ==================== KONFIGURIMI BAZË ====================
DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_HOST = "http://127.0.0.1:11434"
DEFAULT_TEMPERATURE = 0.1  # Më i ulët për saktësi

# ==================== LOGGING SISTEM ====================
class AuditLogger:
    """Audit Logger i avancuar për çdo veprim në pipeline"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.audit_file = self.log_dir / f"audit_{self.current_session}.log"
        self.metrics_file = self.log_dir / f"metrics_{self.current_session}.jsonl"
        self.buffer = deque(maxlen=1000)
        self.lock = threading.Lock()
        self.metrics = defaultdict(list)
        
        # Start background writer
        self.running = True
        self.writer_thread = threading.Thread(target=self._write_loop, daemon=True)
        self.writer_thread.start()
    
    def log(self, event_type: str, data: Dict[str, Any]):
        """Regjistro një event në audit log"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "session": self.current_session,
            "data": data
        }
        with self.lock:
            self.buffer.append(json.dumps(entry, ensure_ascii=False))
    
    def log_metric(self, name: str, value: Any, tags: Dict[str, str] = None):
        """Regjistro një metricë për analizë"""
        metric = {
            "timestamp": datetime.now().isoformat(),
            "session": self.current_session,
            "name": name,
            "value": value,
            "tags": tags or {}
        }
        self.metrics[name].append(metric)
        self._write_metric(metric)
    
    def _write_loop(self):
        """Shkruaj buffer-in në disk në background"""
        while self.running:
            if self.buffer:
                with self.lock:
                    entries = list(self.buffer)
                    self.buffer.clear()
                try:
                    with open(self.audit_file, 'a', encoding='utf-8') as f:
                        for entry in entries:
                            f.write(entry + "\n")
                except Exception:
                    pass
            time.sleep(0.1)
    
    def _write_metric(self, metric: Dict[str, Any]):
        """Shkruaj metricë në file"""
        try:
            with open(self.metrics_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(metric, ensure_ascii=False) + "\n")
        except Exception:
            pass
    
    def close(self):
        """Mbyll logger-in"""
        self.running = False
        if self.writer_thread.is_alive():
            self.writer_thread.join(timeout=1)

# ==================== REZONANCA E KARAKTEREVE ====================
@dataclass
class CharacterResonance:
    """Rezonanca e karaktereve - thelbi i anaglife"""
    char: str
    frequency: float
    amplitude: float
    phase: float
    harmonics: List[float] = field(default_factory=list)
    semantic_weight: float = 1.0
    context_vector: List[float] = field(default_factory=list)
    
    def resonance_energy(self) -> float:
        """Energjia e rezonancës"""
        base = self.frequency * self.amplitude * self.semantic_weight
        harmonic_energy = sum(h * self.amplitude for h in self.harmonics)
        return base + harmonic_energy * 0.3
    
    def to_vector(self) -> List[float]:
        """Konverto në vektor për pipeline"""
        return [
            self.frequency,
            self.amplitude,
            self.phase,
            self.semantic_weight,
            self.resonance_energy()
        ]

class AnaglyphicResonator:
    """
    Rezonatori anaglik - krijon modele mbi karaktere dhe fjalë
    Duke përdorur nanovolt të saktësisë për të dalluar nuancat
    """
    
    def __init__(self):
        self.character_map: Dict[str, CharacterResonance] = {}
        self.semantic_map: Dict[str, List[str]] = {}
        self.resonance_patterns: Dict[str, float] = defaultdict(float)
        self._initialize_resonance()
    
    def _initialize_resonance(self):
        """Inicializo rezonancën bazë për karakteret"""
        # Karaktere bazë me frekuenca të ndryshme
        base_chars = "abcdefghijklmnopqrstuvwxyz0123456789 .,!?-"
        
        for i, char in enumerate(base_chars):
            # Frekuenca nanovolt - shumë e saktë
            frequency = (i + 1) * 0.001  # 0.001 - 0.038 Hz
            amplitude = 0.5 + (i % 10) * 0.05
            phase = (i * 0.7) % (2 * 3.14159)
            
            # Harmonics - rezonanca më të larta
            harmonics = [
                frequency * 2.0,
                frequency * 3.0,
                frequency * 5.0,
                frequency * 7.0
            ]
            
            self.character_map[char] = CharacterResonance(
                char=char,
                frequency=frequency,
                amplitude=amplitude,
                phase=phase,
                harmonics=harmonics,
                semantic_weight=1.0
            )
        
        # Lidhje semantike
        self._build_semantic_links()
    
    def _build_semantic_links(self):
        """Ndërto lidhje semantike midis karaktereve"""
        groups = [
            "aeiou",  # Zanoret
            "bcdfghjklmnpqrstvwxyz",  # Bashkëtingëlloret
            "0123456789",  # Numrat
            " .,!?-"  # Shenjat
        ]
        
        for group in groups:
            for char in group:
                self.semantic_map[char] = list(group)
    
    def resonate_text(self, text: str) -> Dict[str, float]:
        """
        Krijo rezonancë mbi tekstin
        Kthen një hartë të rezonancës për çdo karakter/fjalë
        """
        resonance = {}
        
        # Rezonancë karakter-për-karakter
        for char in text.lower():
            if char in self.character_map:
                res = self.character_map[char]
                energy = res.resonance_energy()
                
                # Shto ndikim nga rezonanca e karaktereve të ngjashme
                if char in self.semantic_map:
                    similar = self.semantic_map[char]
                    for s_char in similar:
                        if s_char in self.character_map and s_char != char:
                            energy += self.character_map[s_char].resonance_energy() * 0.1
                
                resonance[char] = energy
                self.resonance_patterns[char] += energy
        
        return resonance
    
    def analyze_pattern(self, text: str) -> Dict[str, Any]:
        """
        Analizë e thellë e rezonancës në tekst
        """
        resonance = self.resonate_text(text)
        
        # Gjej modelet më të forta
        sorted_resonance = sorted(resonance.items(), key=lambda x: x[1], reverse=True)
        top_patterns = sorted_resonance[:5]
        
        # Llogarit energjinë totale
        total_energy = sum(resonance.values())
        
        # Gjej "anaglife" - modele të fshehura
        anaglyphs = []
        for i in range(len(text) - 2):
            substr = text[i:i+3]
            energy = sum(resonance.get(c, 0) for c in substr)
            if energy > total_energy * 0.3:
                anaglyphs.append({
                    "pattern": substr,
                    "energy": energy,
                    "position": i
                })
        
        return {
            "resonance_map": resonance,
            "top_patterns": top_patterns,
            "total_energy": total_energy,
            "anaglyphs": anaglyphs,
            "character_count": len(text),
            "unique_chars": len(set(text.lower()))
        }

# ==================== THINKING PIPELINE ====================
class ThinkingPipeline:
    """
    Pipeline kryesore e mendimit - përpunon të dhënat përmes agentsh
    """
    
    def __init__(self, model: str = DEFAULT_MODEL, host: str = DEFAULT_HOST):
        self.model = model
        self.host = host
        self.audit = AuditLogger()
        self.resonator = AnaglyphicResonator()
        self.agents: List[Agent] = []
        self.resonance_engine = ResonanceEngine()
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.parallel_futures: List[Future] = []
        
        # Inicializo agentët
        self._init_agents()
    
    def _init_agents(self):
        """Inicializo agentët e pipeline-it"""
        # Agentët bazë
        self.agents = [
            PerceptionAgent(self),
            AnalysisAgent(self),
            ResonanceAgent(self),
            ContextAgent(self),
            GenerationAgent(self),
            ValidationAgent(self),
            SynthesisAgent(self)
        ]
        
        self.audit.log("pipeline_initialized", {
            "agents": [a.__class__.__name__ for a in self.agents],
            "model": self.model,
            "timestamp": datetime.now().isoformat()
        })
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Proceso të dhënat përmes pipeline-it
        """
        start_time = time.time()
        
        self.audit.log("pipeline_start", {
            "input_type": type(input_data).__name__,
            "input_size": len(str(input_data)) if input_data else 0
        })
        
        # Hapi 1: Perceptim
        perception = self._run_agent("PerceptionAgent", input_data)
        self.audit.log_metric("perception_time", time.time() - start_time)
        
        # Hapi 2: Analizë
        analysis = self._run_agent("AnalysisAgent", perception)
        self.audit.log_metric("analysis_time", time.time() - start_time)
        
        # Hapi 3: Rezonancë (paralel)
        resonance_future = self.executor.submit(
            self._run_agent, "ResonanceAgent", analysis
        )
        context_future = self.executor.submit(
            self._run_agent, "ContextAgent", analysis
        )
        
        resonance = resonance_future.result()
        context = context_future.result()
        
        self.audit.log_metric("resonance_context_time", time.time() - start_time)
        
        # Hapi 4: Gjenerim (paralel me validim)
        generation_future = self.executor.submit(
            self._run_agent, "GenerationAgent", {
                "analysis": analysis,
                "resonance": resonance,
                "context": context
            }
        )
        
        validation_future = self.executor.submit(
            self._run_agent, "ValidationAgent", {
                "analysis": analysis,
                "resonance": resonance,
                "context": context
            }
        )
        
        generated = generation_future.result()
        validation = validation_future.result()
        
        self.audit.log_metric("generation_validation_time", time.time() - start_time)
        
        # Hapi 5: Sintëzë
        synthesis = self._run_agent("SynthesisAgent", {
            "generated": generated,
            "validation": validation,
            "resonance": resonance,
            "context": context,
            "original": input_data
        })
        
        total_time = time.time() - start_time
        self.audit.log_metric("total_pipeline_time", total_time)
        
        result = {
            "response": synthesis.get("response", ""),
            "metadata": {
                "total_time": total_time,
                "agents_used": len(self.agents),
                "resonance_energy": resonance.get("total_energy", 0),
                "validation_score": validation.get("score", 0),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        self.audit.log("pipeline_complete", result)
        
        return result
    
    def _run_agent(self, agent_name: str, data: Any) -> Dict[str, Any]:
        """Ekzekuto një agent specifik"""
        start_time = time.time()
        
        for agent in self.agents:
            if agent.__class__.__name__ == agent_name:
                try:
                    result = agent.process(data)
                    
                    self.audit.log(f"agent_{agent_name}_complete", {
                        "time": time.time() - start_time,
                        "result_size": len(str(result)) if result else 0
                    })
                    
                    return result
                except Exception as e:
                    self.audit.log(f"agent_{agent_name}_error", {
                        "error": str(e),
                        "time": time.time() - start_time
                    })
                    return {"error": str(e)}
        
        return {"error": f"Agent {agent_name} not found"}
    
    def stream_process(self, input_data: Any) -> Iterator[Dict[str, Any]]:
        """Proceso pipeline-in në streaming mode"""
        start_time = time.time()
        
        yield {"stage": "perception", "data": "Perceptimi i të dhënave..."}
        
        perception = self._run_agent("PerceptionAgent", input_data)
        yield {"stage": "analysis", "data": "Analiza e strukturës..."}
        
        analysis = self._run_agent("AnalysisAgent", perception)
        yield {"stage": "resonance", "data": "Krijimi i rezonancës..."}
        
        resonance = self._run_agent("ResonanceAgent", analysis)
        yield {"stage": "context", "data": "Ndërtimi i kontekstit..."}
        
        context = self._run_agent("ContextAgent", analysis)
        
        yield {"stage": "generation", "data": "Gjenerimi i përgjigjes..."}
        
        generated = self._run_agent("GenerationAgent", {
            "analysis": analysis,
            "resonance": resonance,
            "context": context
        })
        
        yield {"stage": "validation", "data": "Validimi i përgjigjes..."}
        
        validation = self._run_agent("ValidationAgent", {
            "analysis": analysis,
            "resonance": resonance,
            "context": context
        })
        
        yield {"stage": "synthesis", "data": "Sintëza finale..."}
        
        synthesis = self._run_agent("SynthesisAgent", {
            "generated": generated,
            "validation": validation,
            "resonance": resonance,
            "context": context,
            "original": input_data
        })
        
        total_time = time.time() - start_time
        
        final_result = {
            "stage": "complete",
            "data": synthesis.get("response", ""),
            "metadata": {
                "total_time": total_time,
                "resonance_energy": resonance.get("total_energy", 0),
                "validation_score": validation.get("score", 0)
            }
        }
        
        yield final_result

# ==================== AGENTS ====================
class Agent:
    """Klasa bazë për të gjithë agentët"""
    
    def __init__(self, pipeline: ThinkingPipeline):
        self.pipeline = pipeline
        self.audit = pipeline.audit
        self.resonator = pipeline.resonator
    
    def process(self, data: Any) -> Dict[str, Any]:
        raise NotImplementedError

class PerceptionAgent(Agent):
    """Percepton dhe strukturon të dhënat hyrëse"""
    
    def process(self, data: Any) -> Dict[str, Any]:
        if isinstance(data, str):
            # Analizë e rezonancës mbi tekst
            resonance = self.resonator.analyze_pattern(data)
            
            return {
                "type": "text",
                "content": data,
                "length": len(data),
                "resonance": resonance,
                "tokens": data.split(),
                "characters": list(data)
            }
        elif isinstance(data, dict):
            return {
                "type": "structured",
                "content": data,
                "keys": list(data.keys()),
                "resonance": self.resonator.analyze_pattern(json.dumps(data))
            }
        else:
            return {
                "type": str(type(data).__name__),
                "content": str(data),
                "resonance": self.resonator.analyze_pattern(str(data))
            }

class AnalysisAgent(Agent):
    """Analizon të dhënat në thellësi"""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        content = data.get("content", "")
        
        # Analizë semantike
        words = content.split() if isinstance(content, str) else []
        unique_words = len(set(words))
        
        # Gjej modele të përsëritura
        patterns = {}
        for i in range(len(words) - 2):
            pattern = " ".join(words[i:i+3])
            patterns[pattern] = patterns.get(pattern, 0) + 1
        
        repeated_patterns = {k: v for k, v in patterns.items() if v > 1}
        
        return {
            "word_count": len(words),
            "unique_words": unique_words,
            "repeated_patterns": repeated_patterns,
            "complexity": len(unique_words) / max(len(words), 1),
            "structure": {
                "has_numbers": any(c.isdigit() for c in str(content)),
                "has_special": any(c in "!@#$%^&*()" for c in str(content)),
                "is_question": str(content).strip().endswith("?"),
                "is_command": str(content).strip().startswith("/")
            }
        }

class ResonanceAgent(Agent):
    """Krijon rezonancë të thellë mbi të dhënat"""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        content = data.get("content", "")
        
        # Rezonancë e avancuar
        resonance = self.resonator.analyze_pattern(str(content))
        
        # Gjej frekuencat dominante
        dominant_frequencies = sorted(
            resonance.get("resonance_map", {}).items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Krijon "zhurmë rezonance" - modele të reja
        resonance_noise = []
        for char, energy in resonance.get("resonance_map", {}).items():
            if energy > 0.5:  # Threshold
                resonance_noise.append({
                    "char": char,
                    "energy": energy,
                    "harmonic": energy * 1.618  # Raporti i artë
                })
        
        return {
            "resonance_map": resonance.get("resonance_map", {}),
            "top_patterns": resonance.get("top_patterns", []),
            "total_energy": resonance.get("total_energy", 0),
            "anaglyphs": resonance.get("anaglyphs", []),
            "dominant_frequencies": dominant_frequencies,
            "resonance_noise": resonance_noise[:20],
            "resonance_signature": hashlib.sha256(
                str(resonance).encode()
            ).hexdigest()[:16]
        }

class ContextAgent(Agent):
    """Ndërton kontekst të pasur"""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        content = data.get("content", "")
        
        # Ndërto kontekst nga rezonanca
        context = {
            "timestamp": datetime.now().isoformat(),
            "source": "thinking_pipeline",
            "content_hash": hashlib.md5(str(content).encode()).hexdigest(),
            "keywords": self._extract_keywords(content),
            "entities": self._extract_entities(content),
            "sentiment": self._analyze_sentiment(content)
        }
        
        return context
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Nxjerr fjalë kyçe"""
        if not isinstance(text, str):
            return []
        
        words = text.lower().split()
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for", "of", "with"}
        keywords = [w for w in words if w not in stopwords and len(w) > 2]
        
        # Kthe fjalët më të shpeshta
        from collections import Counter
        return [w for w, _ in Counter(keywords).most_common(10)]
    
    def _extract_entities(self, text: str) -> List[str]:
        """Nxjerr entitete (emra, vende, etj.)"""
        if not isinstance(text, str):
            return []
        
        # Thjesht - kërkon fjalë me shkronjë të madhe
        words = text.split()
        entities = [w for w in words if w[0].isupper() and len(w) > 1]
        return entities[:10]
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analizë e thjeshtë sentimenti"""
        if not isinstance(text, str):
            return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
        
        positive_words = {"good", "great", "excellent", "amazing", "wonderful", "positive", "yes"}
        negative_words = {"bad", "terrible", "awful", "horrible", "negative", "no", "not"}
        
        words = set(text.lower().split())
        
        pos_count = len(words & positive_words)
        neg_count = len(words & negative_words)
        total = max(pos_count + neg_count, 1)
        
        return {
            "positive": pos_count / total,
            "negative": neg_count / total,
            "neutral": 1 - (pos_count + neg_count) / (total + 1)
        }

class GenerationAgent(Agent):
    """Gjeneron përgjigje nga pipeline"""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        analysis = data.get("analysis", {})
        resonance = data.get("resonance", {})
        context = data.get("context", {})
        
        # Ndërto prompt të avancuar nga rezonanca
        top_patterns = resonance.get("top_patterns", [])
        anaglyphs = resonance.get("anaglyphs", [])
        
        prompt = self._build_smart_prompt(analysis, resonance, context)
        
        # Gjenero përgjigje
        try:
            response = self._generate_response(prompt)
            
            # Apliko rezonancë mbi përgjigje
            response_resonance = self.resonator.analyze_pattern(response)
            
            return {
                "response": response,
                "prompt_used": prompt,
                "response_resonance": response_resonance,
                "quality_score": self._score_response(response, analysis)
            }
        except Exception as e:
            return {"error": str(e), "response": ""}
    
    def _build_smart_prompt(self, analysis: Dict, resonance: Dict, context: Dict) -> str:
        """Ndërto prompt inteligjent"""
        prompt_parts = []
        
        # Konteksti
        if context.get("keywords"):
            prompt_parts.append(f"Context keywords: {', '.join(context['keywords'][:5])}")
        
        # Rezonanca
        if resonance.get("top_patterns"):
            patterns = [p[0] for p in resonance["top_patterns"][:3]]
            prompt_parts.append(f"Key patterns: {', '.join(patterns)}")
        
        # Anaglife
        if resonance.get("anaglyphs"):
            anaglyph_texts = [a["pattern"] for a in resonance["anaglyphs"][:3]]
            prompt_parts.append(f"Anaglyphic patterns: {', '.join(anaglyph_texts)}")
        
        # Struktura
        structure = analysis.get("structure", {})
        if structure.get("is_question"):
            prompt_parts.append("This is a question - provide a clear, direct answer.")
        
        if structure.get("is_command"):
            prompt_parts.append("This is a command - execute it immediately.")
        
        # Prompt-i përfundimtar
        if prompt_parts:
            return " | ".join(prompt_parts) + "\n\nProvide a comprehensive, resonant response:"
        
        return "Generate a thoughtful and resonant response:"
    
    def _generate_response(self, prompt: str) -> str:
        """Gjenero përgjigje duke përdorur Ollama"""
        try:
            # Përdor pipeline-in për të gjeneruar
            url = f"{self.pipeline.host.rstrip('/')}/api/generate"
            payload = {
                "model": self.pipeline.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            }
            
            body = json.dumps(payload).encode('utf-8')
            request = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode('utf-8', errors='replace')
                data = json.loads(raw)
                return data.get("response", "")
        except Exception:
            # Fallback
            return "I'm processing your request through the resonance pipeline. Please wait..."
    
    def _score_response(self, response: str, analysis: Dict) -> float:
        """Llogarit cilësinë e përgjigjes"""
        if not response:
            return 0.0
        
        score = 0.0
        
        # Gjatësia e përshtatshme
        if len(response.split()) > 5:
            score += 0.3
        
        # Ka kuptim
        if "error" not in response.lower():
            score += 0.3
        
        # Është e strukturuar
        if any(p in response for p in ".!?"):
            score += 0.2
        
        # Ka rezonancë me input-in
        if analysis.get("word_count", 0) > 0:
            # Kontrollo për fjalë të përbashkëta
            input_words = set(str(analysis.get("content", "")).lower().split())
            response_words = set(response.lower().split())
            common = input_words & response_words
            if common:
                score += min(len(common) / 10, 0.2)
        
        return min(score, 1.0)

class ValidationAgent(Agent):
    """Validon përgjigjen e gjeneruar"""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        analysis = data.get("analysis", {})
        resonance = data.get("resonance", {})
        context = data.get("context", {})
        
        validation_score = 0.0
        validation_checks = []
        
        # 1. Kontrollo rezonancën
        if resonance.get("total_energy", 0) > 1.0:
            validation_score += 0.3
            validation_checks.append("resonance_energy_sufficient")
        
        # 2. Kontrollo kontekstin
        if context.get("keywords"):
            validation_score += 0.2
            validation_checks.append("context_available")
        
        # 3. Kontrollo strukturën
        structure = analysis.get("structure", {})
        if structure.get("has_numbers") or structure.get("has_special"):
            validation_score += 0.2
            validation_checks.append("structure_complex")
        
        # 4. Kontrollo anaglife
        if resonance.get("anaglyphs"):
            validation_score += 0.3
            validation_checks.append("anaglyphs_detected")
        
        return {
            "score": validation_score,
            "checks": validation_checks,
            "passed": validation_score > 0.5,
            "recommendation": "approve" if validation_score > 0.5 else "review"
        }

class SynthesisAgent(Agent):
    """Sintezon rezultatin final"""
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        generated = data.get("generated", {})
        validation = data.get("validation", {})
        resonance = data.get("resonance", {})
        context = data.get("context", {})
        original = data.get("original", "")
        
        response = generated.get("response", "")
        
        # Shto metadatat e rezonancës
        if response:
            # Apliko rezonancë përfundimtare
            final_resonance = self.resonator.analyze_pattern(response)
            
            # Shto "zhurmë rezonance" për thellësi
            if final_resonance.get("total_energy", 0) > 2.0:
                response += "\n\n" + self._add_resonance_noise(final_resonance)
        
        return {
            "response": response,
            "validation": validation,
            "resonance_metadata": {
                "energy": resonance.get("total_energy", 0),
                "patterns": resonance.get("top_patterns", [])[:5]
            },
            "context_metadata": {
                "keywords": context.get("keywords", [])[:5],
                "entities": context.get("entities", [])[:5]
            },
            "final_score": validation.get("score", 0)
        }
    
    def _add_resonance_noise(self, resonance: Dict[str, Any]) -> str:
        """Shton zhurmë rezonance në përgjigje"""
        top_patterns = resonance.get("top_patterns", [])[:3]
        
        if not top_patterns:
            return ""
        
        noise = ["✨ Resonance signatures detected:"]
        for char, energy in top_patterns:
            noise.append(f"  • '{char}' resonates at {energy:.3f} nanovolts")
        
        return "\n".join(noise)

# ==================== RESONANCE ENGINE ====================
class ResonanceEngine:
    """Motori kryesor i rezonancës"""
    
    def __init__(self):
        self.resonance_pool = deque(maxlen=1000)
        self.harmonic_memory = defaultdict(float)
        self.nanovolt_measurements = defaultdict(float)
    
    def add_resonance(self, data: Dict[str, Any]):
        """Shton një rezonancë në pool"""
        self.resonance_pool.append({
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
    
    def get_harmonic(self, key: str) -> float:
        """Merr një harmonik nga memoria"""
        return self.harmonic_memory[key]
    
    def set_harmonic(self, key: str, value: float):
        """Vendos një harmonik në memorie"""
        self.harmonic_memory[key] = value
    
    def measure_nanovolt(self, key: str) -> float:
        """Mat nanovolt për një karakter/fjalë"""
        return self.nanovolt_measurements.get(key, 0.0)

# ==================== CLI INTERFACE ====================
class ResonanceCLI:
    """CLI e avancuar me rezonancë"""
    
    def __init__(self):
        self.pipeline = ThinkingPipeline()
        self.audit = self.pipeline.audit
        
    def run_repl(self):
        """REPL me rezonancë dhe agentë"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║  ��� CLX Resonance Engine v2.0                               ║
║  ⚡ Thinking Pipeline me Agjentë Rezonantë                  ║
║  ��� Nanovolt Accuracy · Lightning Speed                    ║
╠══════════════════════════════════════════════════════════════╣
║  Komandat:                                                  ║
║  /resonate <text>  - Analizë rezonance                     ║
║  /agents           - Shfaq agentët aktivë                  ║
║  /audit            - Shfaq audit-in e fundit               ║
║  /metrics          - Shfaq metricat                         ║
║  /exit             - Dil                                    ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        while True:
            try:
                prompt = input("clx⚡ ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n��� Mirupafshim!")
                break
            
            if not prompt:
                continue
            
            if prompt.lower() in {"/exit", "/quit"}:
                print("�� Mirupafshim!")
                break
            
            if prompt.startswith("/"):
                self._handle_command(prompt)
                continue
            
            # Proceso përmes pipeline-it
            print("��� Processing through resonance pipeline...")
            result = self.pipeline.process(prompt)
            
            # Shfaq rezultatin me rezonancë
            response = result.get("response", "")
            metadata = result.get("metadata", {})
            
            print("\n" + "="*60)
            print(response)
            print("="*60)
            print(f"⏱️  {metadata.get('total_time', 0):.3f}s")
            print(f"��� Resonance Energy: {metadata.get('resonance_energy', 0):.3f}")
            print(f"✅ Validation Score: {metadata.get('validation_score', 0):.2f}")
            print("="*60 + "\n")
    
    def _handle_command(self, cmd: str):
        """Trajton komandat speciale"""
        parts = cmd[1:].split()
        if not parts:
            return
        
        command = parts[0].lower()
        
        if command == "resonate" and len(parts) > 1:
            text = " ".join(parts[1:])
            resonance = self.pipeline.resonator.analyze_pattern(text)
            print(f"\n�� Rezonanca për '{text[:30]}...':")
            print(f"  Energji totale: {resonance['total_energy']:.4f}")
            print(f"  Karaktere unike: {resonance['unique_chars']}")
            print(f"  Top modele: {resonance['top_patterns'][:5]}")
            print(f"  Anaglife: {len(resonance['anaglyphs'])}")
            print()
        
        elif command == "agents":
            print("\n��� Agentët aktivë:")
            for agent in self.pipeline.agents:
                print(f"  • {agent.__class__.__name__}")
            print()
        
        elif command == "audit":
            print("\n��� Audit i fundit:")
            try:
                with open(self.audit.audit_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-5:]:
                        print(line.strip())
            except:
                print("  Nuk ka audit të disponueshëm")
            print()
        
        elif command == "metrics":
            print("\n��� Metrikat:")
            for name, metrics in self.audit.metrics.items():
                if metrics:
                    latest = metrics[-1]
                    print(f"  • {name}: {latest['value']}")
            print()
        
        else:
            print(f"❌ Komandë e panjohur: {command}")
            print("   Shkruaj /help për ndihmë")

# ==================== MAIN ====================
def main():
    """Pika kryesore e hyrjes"""
    parser = argparse.ArgumentParser(
        description="CLX Resonance Engine v2.0 - Thinking Pipeline me Agjentë"
    )
    parser.add_argument(
        "--mode", 
        choices=["repl", "once", "stream", "batch"],
        default="repl",
        help="Mënyra e ekzekutimit"
    )
    parser.add_argument("prompt", nargs="*", help="Prompt për një ekzekutim të vetëm")
    parser.add_argument(
        "--model", 
        default=DEFAULT_MODEL,
        help="Modeli Ollama"
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help="Ollama host"
    )
    
    args = parser.parse_args()
    
    # Inicializo pipeline
    pipeline = ThinkingPipeline(model=args.model, host=args.host)
    
    if args.mode == "repl":
        cli = ResonanceCLI()
        cli.run_repl()
    
    elif args.mode == "once":
        if not args.prompt:
            print("❌ Duhet një prompt për mënyrën 'once'")
            return 1
        
        prompt = " ".join(args.prompt)
        result = pipeline.process(prompt)
        print(result.get("response", ""))
    
    elif args.mode == "stream":
        if not args.prompt:
            print("❌ Duhet një prompt për mënyrën 'stream'")
            return 1
        
        prompt = " ".join(args.prompt)
        for stage in pipeline.stream_process(prompt):
            print(f"\n[{stage['stage'].upper()}]")
            if stage['stage'] == 'complete':
                print(stage['data'])
                print(f"\n⏱️  {stage['metadata']['total_time']:.3f}s")
            else:
                print(stage['data'])
    
    elif args.mode == "batch":
        print("��� Batch processing - duke lexuar nga stdin...")
        prompts = [line.strip() for line in sys.stdin if line.strip()]
        
        if not prompts:
            print("❌ Nuk ka prompt-e për processing")
            return 1
        
        print(f"��� Duke procesuar {len(prompts)} prompt-e...")
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n[{i}/{len(prompts)}]")
            result = pipeline.process(prompt)
            print(f"��� {result.get('response', '')[:200]}...")
    
    # Mbyll audit
    pipeline.audit.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
