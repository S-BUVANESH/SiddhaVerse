# API Documentation Report — SiddhaVerse v1.1.0

**Base URL**: `http://localhost:8000`  
**Swagger UI**: `/docs`  
**ReDoc**: `/redoc`  
**OpenAPI Schema**: `/openapi.json`

---

## Endpoint Reference

### Observability

| Method | Path | Description |
| :--- | :--- | :--- |
| GET | `/health` | Liveness probe. Returns DB status and document count. |
| GET | `/ready` | Readiness probe. Returns 503 if corpus not loaded. |

**Health response example**:
```json
{
  "status": "success",
  "version": "1.1",
  "data": {
    "status": "healthy",
    "database_connected": true,
    "document_count": 1174,
    "environment": "production",
    "version": "1.1.0",
    "latency_ms": 2
  }
}
```

---

### Search

| Method | Path | Description |
| :--- | :--- | :--- |
| GET | `/api/v1/search` | Multi-mode search (lexical / vector / hybrid) |

**Key parameters**:

| Parameter | Type | Values |
| :--- | :--- | :--- |
| `q` | string | Search query (Tamil, Romanized, English) |
| `mode` | enum | `lexical` _(default)_ \| `vector` \| `hybrid` |
| `doc_type` | enum | `all` \| `verse` \| `biography` \| `plant` \| `formulation` \| `manuscript` \| `research` |
| `work` | enum | `all` \| `Thirumandiram` \| `Sivavakkiyam` |
| `page` | int ≥ 1 | Page number |
| `per_page` | int 1–100 | Results per page |
| `sort` | enum | `relevance` \| `verse_number` \| `work` \| `author` |

---

### Corpus Lookups

| Method | Path | Description |
| :--- | :--- | :--- |
| GET | `/api/v1/verse/{id}` | Single verse by document ID |
| GET | `/api/v1/verse/random` | Random verse (filterable by work / entity) |
| GET | `/api/v1/entity/{id}` | Entity metadata (plant, herb, concept, person) |
| GET | `/api/v1/plant/{id}` | Medicinal plant profile |
| GET | `/api/v1/siddhar/{id}` | Siddhar biography |
| GET | `/api/v1/work/{id}` | Classical work verse index (paginated) |
| GET | `/api/v1/formulation/{id}` | Medicine formulation with ingredients |
| GET | `/api/v1/collections` | Corpus metadata and document type counts |

---

### RAG (Citation-Constrained)

| Method | Path | Body | Description |
| :--- | :--- | :--- | :--- |
| GET | `/api/v1/rag` | — | RAG query via `q` parameter |
| POST | `/api/v1/rag` | `{"query": "..."}` | RAG query via JSON body |

**RAG response example**:
```json
{
  "status": "success",
  "data": {
    "answer": "Kayakalpa refers to body rejuvenation practices... <cite doc=\"thirumandiram_pm_0741\" hash=\"a3f2...\" />",
    "citations": [
      {
        "document_id": "thirumandiram_pm_0741",
        "source_work": "Thirumandiram",
        "verse_number": "741",
        "source_url": null
      }
    ],
    "intent": {"category": "verse_lookup", "confidence": 0.91},
    "retrieval_count": 5
  }
}
```

**Refusal example**:
```json
{
  "status": "success",
  "data": {
    "answer": "The corpus does not contain sufficient evidence to answer this query.",
    "citations": [],
    "refused": true
  }
}
```

---

## Standard Response Envelope

All endpoints return:
```json
{
  "status": "success" | "error",
  "version": "1.1",
  "timestamp": "2026-06-29T12:00:00Z",
  "data": { ... },
  "meta": { ... }
}
```

## Standard Response Headers

| Header | Description |
| :--- | :--- |
| `X-Request-ID` | Unique request trace ID |
| `X-Response-Time-Ms` | Request processing duration |

## Error Codes

| Status | Meaning |
| :--- | :--- |
| 200 | Success |
| 404 | Document / entity not found |
| 422 | Validation error (invalid parameter) |
| 429 | Rate limit exceeded |
| 503 | Service not ready (readiness probe) |
