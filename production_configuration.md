# Production Configuration — SiddhaVerse

**Version**: 1.1.0

---

## Environment Profiles

### Development (default)
```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
STRUCTURED_LOGGING=false
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=200
ALLOWED_ORIGINS=*
API_KEY_REQUIRED=false
DB_PATH=d:\Siddha_Wisdom\siddhaverse.db
```

### Staging
```env
ENVIRONMENT=staging
LOG_LEVEL=INFO
STRUCTURED_LOGGING=true
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=120
ALLOWED_ORIGINS=https://staging.siddhaverse.app
API_KEY_REQUIRED=false
DB_PATH=/data/corpus/siddhaverse.db
```

### Production
```env
ENVIRONMENT=production
LOG_LEVEL=INFO
STRUCTURED_LOGGING=true
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_WINDOW_SECONDS=60
ALLOWED_ORIGINS=https://siddhaverse.app,https://api.siddhaverse.app
API_KEY_REQUIRED=false
DB_PATH=/data/corpus/siddhaverse.db
MAX_CONTEXT_TOKENS=4000
RRF_LEXICAL_WEIGHT=0.70
RRF_VECTOR_WEIGHT=0.30
ENABLE_RERANKER=false
STRUCTURED_LOGGING=true
```

---

## All Configuration Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `ENVIRONMENT` | `development` | Runtime environment label |
| `LOG_LEVEL` | `INFO` | Python logging level |
| `STRUCTURED_LOGGING` | `false` | JSON log format for aggregators |
| `API_PREFIX` | `/api/v1` | API route prefix |
| `DB_TYPE` | `sqlite` | `sqlite` or `postgres` |
| `DB_PATH` | _(hardcoded)_ | Path to SQLite corpus DB |
| `POSTGRES_DSN` | — | PostgreSQL connection string |
| `MAX_CONTEXT_TOKENS` | `4000` | RAG context budget |
| `GEMINI_API_KEY` | _(unset)_ | Enables Gemini 1.5 Pro inference |
| `GEMINI_MODEL` | `gemini-1.5-pro` | Gemini model variant |
| `RRF_LEXICAL_WEIGHT` | `1.0` | BM25 RRF fusion weight |
| `RRF_VECTOR_WEIGHT` | `1.0` | Vector RRF fusion weight |
| `ENABLE_RERANKER` | `true` | Cross-encoder reranking toggle |
| `RERANKER_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Cross-encoder model |
| `RATE_LIMIT_ENABLED` | `true` | Rate limiting toggle |
| `RATE_LIMIT_REQUESTS` | `60` | Max requests per window |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` | Sliding window size |
| `API_KEY_REQUIRED` | `false` | Require `X-API-Key` header |
| `ALLOWED_ORIGINS` | `*` | CORS origin whitelist |
| `REQUEST_ID_HEADER` | `X-Request-ID` | Request tracing header name |

---

## Docker Resource Recommendations

| Tier | RAM | CPU | Notes |
| :--- | :--- | :--- | :--- |
| Minimum | 4 GB | 2 vCPU | Simulator LLM, no reranker |
| Recommended | 8 GB | 4 vCPU | Gemini API + E5-large embeddings |
| Full (with reranker) | 12 GB | 4 vCPU | Cross-encoder loaded at startup |

---

## Backup & Restore

```bash
# Backup
cp siddhaverse.db backups/siddhaverse.db.$(Get-Date -Format "yyyyMMdd")

# Restore
docker-compose down
cp backups/siddhaverse.db.YYYYMMDD siddhaverse.db
docker-compose up -d

# Verify
curl http://localhost:8000/ready
```
