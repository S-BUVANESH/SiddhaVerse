# Security Hardening Report — SiddhaVerse v1.1.0

**Date**: 2026-06-29  
**Scope**: API layer (backend/app/)

---

## 1. Rate Limiting

| Property | Value |
| :--- | :--- |
| Algorithm | Sliding window (per client IP) |
| Default limit | 60 req / 60 seconds |
| Response on breach | HTTP 429 + JSON error body |
| Configuration | `RATE_LIMIT_ENABLED`, `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW_SECONDS` |
| Bypass | Disabled via `RATE_LIMIT_ENABLED=false` (dev only) |

> [!NOTE]
> Current implementation is in-memory and per-process. For multi-worker deployments,
> migrate to Redis-backed rate limiting (e.g., `slowapi` + Redis) before production scale-out.

---

## 2. CORS

| Setting | Current | Production Recommendation |
| :--- | :--- | :--- |
| `ALLOWED_ORIGINS` | `*` (open beta) | `https://siddhaverse.app` |
| Methods | `GET, POST` | Unchanged |
| Credentials | `true` | Unchanged |

---

## 3. Citation Verification (Anti-Hallucination)

| Property | Detail |
| :--- | :--- |
| Mechanism | SHA-256 content hash per document |
| Check 1 | `doc_id` must exist in injected context map |
| Check 2 | `hash` must match stored content hash exactly |
| Action on failure | Entire response blocked; warning logged |
| Client exposure | Hash value excluded from client response |

---

## 4. Input Validation

| Concern | Mitigation |
| :--- | :--- |
| Query parameter types | FastAPI Pydantic validation — invalid types return HTTP 422 |
| Path parameter injection | Path values are validated before DB query |
| Prompt injection in RAG | System prompt anchors context strictly; LLM cannot break citation constraints without triggering CitationVerifier |
| Nonsense / OOD queries | Lexical pre-check + 0.82 vector similarity gate refuse gracefully before LLM invocation |

---

## 5. Request Tracing

- Every request receives a `X-Request-ID` (UUID prefix)
- Logged at middleware level for full audit trail
- Returned in response headers for client-side debugging

---

## 6. Database Security

| Property | Value |
| :--- | :--- |
| Access mode | Read-only volume mount in Docker (`siddhaverse.db:ro`) |
| SQL injection | No raw SQL in user queries; FTS5 parameterized queries throughout |
| Credentials | No DB credentials needed for SQLite mode |

---

## 7. Known Limitations (Beta)

| Limitation | Risk | Mitigation |
| :--- | :--- | :--- |
| In-memory rate limiter | Resets on restart; ineffective across workers | Redis backend before scale-out |
| `ALLOWED_ORIGINS=*` | Cross-origin requests from any domain | Set explicit origin list before public launch |
| `API_KEY_REQUIRED=false` | Public access with no auth | Add API key gate or OAuth for production |
| Starlette `httpx` deprecation | Third-party test client warning | `pip install httpx2` when upgrading FastAPI |
| Gemini API key exposure | Key in `.env` file | Use secrets manager (AWS Secrets Manager / Vault) in production |

---

## 8. Recommended Production Security Actions

- [ ] Set `ALLOWED_ORIGINS` to explicit domain list
- [ ] Enable `API_KEY_REQUIRED=true` with key rotation policy
- [ ] Move `GEMINI_API_KEY` to secrets manager
- [ ] Replace in-memory rate limiter with Redis-backed `slowapi`
- [ ] Add nginx / Caddy reverse proxy with TLS termination
- [ ] Enable fail2ban or WAF for brute-force protection
- [ ] Add Sentry / OpenTelemetry tracing for request spans
