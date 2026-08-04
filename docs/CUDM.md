# CLISONIX UNIFIED DATA MODEL (CUDM) v1.0
## Modeli i Unifikuar i të Dhënave

### Parimi:
> "Të gjitha modulet flasin të njëjtën gjuhë të dhënash pa konflikte."

---

## 1. STRUKTURA BAZË E TË DHËNAVE

### 1.1 Data Packet (Paketa e të Dhënave)
```json
{
  "id": "string (hash)",
  "type": "string (memory|agent|task|event|message|knowledge)",
  "timestamp": "ISO 8601 datetime",
  "source": "string (moduli që e krijoi)",
  "version": "integer",
  "payload": {},
  "signature": "string (hash i nënshkrimit)"
}
```

### 1.2 Node Identity (Identiteti i Nyjës)
```json
{
  "node_id": "string (hash unik)",
  "name": "string",
  "type": "string (desktop|laptop|phone|edge|iot|server)",
  "capabilities": {
    "cpu": {"cores": "integer", "speed": "float"},
    "gpu": {"available": "boolean", "memory": "integer"},
    "ram": {"total": "integer", "available": "integer"},
    "storage": {"total": "integer", "free": "integer"},
    "bandwidth": {"upload": "float", "download": "float"},
    "sensors": ["string list"]
  },
  "location": {"lat": "float", "lon": "float", "region": "string"},
  "status": "string (active|idle|busy|offline)",
  "trust_score": "float (0.0-1.0)",
  "last_seen": "ISO 8601 datetime"
}
```

### 1.3 Memory Entry (Hyrje në Memorie)
```json
{
  "memory_id": "string (hash)",
  "type": "string (horizontal|vertical|orbital|resonance|film|stigma|working|long_term)",
  "key": "string",
  "value": "any",
  "weight": "float (0.0-1.0)",
  "connections": ["string list (memory_ids)"],
  "source": "string",
  "timestamp": "ISO 8601 datetime",
  "ttl": "integer (seconds, -1=përherë)",
  "hash": "string (SHA-256)"
}
```

### 1.4 Agent Message (Mesazh Agjenti)
```json
{
  "agent_id": "string",
  "from": "string",
  "to": "string (agent_id|broadcast)",
  "type": "string (request|response|broadcast|error)",
  "action": "string",
  "payload": {},
  "priority": "integer (1-10)",
  "timestamp": "ISO 8601 datetime",
  "reply_to": "string (optional)"
}
```

### 1.5 Task (Detyrë)
```json
{
  "task_id": "string (hash)",
  "type": "string (research|build|govern|security|protocol|country)",
  "status": "string (pending|running|completed|failed|blocked)",
  "assigned_to": "string (agent_id)",
  "input": {},
  "output": {},
  "priority": "integer (1-10)",
  "dependencies": ["string list (task_ids)"],
  "created": "ISO 8601 datetime",
  "started": "ISO 8601 datetime (nullable)",
  "completed": "ISO 8601 datetime (nullable)",
  "error": "string (nullable)"
}
```

### 1.6 Verification Record (Verifikim)
```json
{
  "verification_id": "string (hash)",
  "data_hash": "string",
  "sources": [
    {"url": "string", "title": "string", "access_date": "ISO 8601", "confidence": "float"}
  ],
  "cross_checked": "boolean",
  "source_count": "integer",
  "verified_by": ["string list (agent_ids)"],
  "timestamp": "ISO 8601 datetime",
  "expires": "ISO 8601 datetime"
}
```

### 1.7 SSE Chunk (Copë SSE)
```json
{
  "chunk_id": "string (hash)",
  "stream_id": "string",
  "sequence": "integer",
  "data": "any",
  "type": "string (text|json|binary|event)",
  "timestamp": "ISO 8601 datetime",
  "final": "boolean"
}
```

---

## 2. PROTOKOLLET E KOMUNIKIMIT

### 2.1 Internal API (Komunikimi Modul-Modul)
```
Metoda: POST
Path: /cudm/v1/{modul}/{veprim}
Body: Data Packet
Response: Data Packet
```

### 2.2 External API (Komunikimi me Botën e Jashtme)
```
Metoda: GET|POST|PUT|DELETE
Path: /api/v1/{resource}
Headers: 
  Authorization: Bearer {token}
  Content-Type: application/json
  X-CUDM-Version: 1.0
```

### 2.3 SSE Stream (Transmetim i Vazhdueshëm)
```
Endpoint: /stream/v1/{stream_id}
Format: 
  event: {event_type}
  data: {json_data}
  id: {chunk_id}
```

### 2.4 Node-to-Node (Mesh)
```
Protokolli: UDP/TCP
Porta: 8765 (default)
Formati: Data Packet i koduar
```

---

## 3. KONVENTAT E EMËRTIMIT

| Lloji | Prefiksi | Shembull |
|-------|----------|----------|
| Memory ID | mem_ | mem_hvo_7a3f |
| Agent ID | agt_ | agt_research_01 |
| Task ID | task_ | task_research_45 |
| Stream ID | str_ | str_main_01 |
| Node ID | node_ | node_desktop_xyz |
| Token | tok_ | tok_user_a1b2 |
| Session | ses_ | ses_user_xyz |
| Event | evt_ | evt_memory_store |

---

## 4. VALIDIMI I TË DHËNAVE

Çdo modul para se të dërgojë të dhëna duhet:
1. Të verifikojë që struktura përputhet me CUDM
2. Të shtojë timestamp dhe source
3. Të gjenerojë hash-in e paketës
4. Të nënshkruajë me çelësin e modulit

---

## 5. VERSIONIMI

- CUDM versioni aktual: 1.0
- Çdo ndryshim rrit versionin minor (1.1, 1.2)
- Ndryshime që prishin përputhshmëri rrisin versionin major (2.0)
- Modulet e vjetra marrin njoftim për migrim automatik

---

*"Asnjë modul nuk komunikon me formatin e vet. Të gjithë përdorin të njëjtin model të të dhënave."*

