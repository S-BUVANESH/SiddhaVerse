# SiddhaVerse Beta Deployment Checklist

**Version**: 1.1.0  
**Target**: Public Beta

---

## Pre-Deployment

### Code & Tests
- [x] All 23 tests passing (`python -m pytest backend/ -q`)
- [x] Zero deprecation warnings remaining
- [x] Pydantic v2 migration complete (`ConfigDict`)
- [x] FastAPI lifespan migration complete
- [x] Embedding API warning resolved (`get_embedding_dimension`)

### Configuration
- [ ] Copy `.env.template` to `.env.production`
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `STRUCTURED_LOGGING=true`
- [ ] Set `LOG_LEVEL=INFO`
- [ ] Set `ALLOWED_ORIGINS=https://siddhaverse.app` (restrict wildcard `*`)
- [ ] Set `GEMINI_API_KEY` (or confirm simulator mode is acceptable for beta)
- [ ] Set `RATE_LIMIT_REQUESTS=60` and `RATE_LIMIT_WINDOW_SECONDS=60`
- [ ] Review `MAX_CONTEXT_TOKENS=4000` (increase to 6000 if Gemini Pro is active)

### Security
- [ ] Remove wildcard `ALLOWED_ORIGINS=*` before public launch
- [ ] Confirm `API_KEY_REQUIRED=false` is intentional for open beta
- [ ] Verify HTTPS is terminated at reverse proxy (nginx / Caddy)
- [ ] Confirm database file permissions: `siddhaverse.db` — read-only mount in Docker
- [ ] Review rate limit thresholds with expected traffic

### Database
- [ ] Backup `siddhaverse.db` before deployment
- [ ] Confirm document count: `GET /ready` → `document_count` ≥ 1000
- [ ] Confirm `GET /health` returns `"database_connected": true`
- [ ] Confirm Qdrant vector DB is accessible (if vector/hybrid search enabled)

---

## Deployment

### Docker
```bash
# Build
docker build -t siddhaverse-api:1.1.0 .

# Verify build
docker run --rm -p 8000:8000 \
  --env-file .env.production \
  -v ./siddhaverse.db:/data/corpus/siddhaverse.db:ro \
  siddhaverse-api:1.1.0

# Run with compose
docker-compose up -d
```

### Health Verification
```bash
curl http://localhost:8000/health
# Expect: {"status":"success","data":{"status":"healthy","database_connected":true,...}}

curl http://localhost:8000/ready
# Expect: {"status":"success","data":{"ready":true,"document_count":...}}

curl "http://localhost:8000/api/v1/search?q=kayakalpa&mode=lexical"
# Expect: results with intent, evidence_package
```

---

## Post-Deployment

### Smoke Tests
- [ ] `GET /health` → `"status":"healthy"`
- [ ] `GET /ready` → `"ready":true`
- [ ] `GET /api/v1/search?q=thirumoolar&mode=hybrid` → results
- [ ] `GET /api/v1/rag?q=What+is+kayakalpa` → answer with citations
- [ ] `POST /api/v1/rag` with JSON body → answer with citations
- [ ] Rate limit test: 61 rapid requests → HTTP 429 on 61st
- [ ] Out-of-scope query → graceful refusal message
- [ ] `/docs` → Swagger UI loads
- [ ] `/redoc` → ReDoc loads

### Monitoring
- [ ] Confirm `X-Request-ID` header present on all responses
- [ ] Confirm `X-Response-Time-Ms` header present on all responses
- [ ] Confirm logs are appearing in `backend_run.log`
- [ ] Set up log aggregation (CloudWatch / Loki / Datadog) consuming JSON logs

### Backup & Restore
```bash
# Backup corpus DB
cp siddhaverse.db siddhaverse.db.bak.$(date +%Y%m%d)

# Restore
cp siddhaverse.db.bak.YYYYMMDD siddhaverse.db
docker-compose restart siddhaverse-api
```

---

## Rollback Plan

1. `docker-compose down`
2. Restore DB from backup
3. `docker run` previous image tag (`siddhaverse-api:1.0.0`)
4. Verify `/health` and `/ready`
