import uuid
import time
import logging
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Depends, Query, HTTPException, Path, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.app.config import settings
from backend.app.repositories import BaseDocumentRepository, SQLiteDocumentRepository
from backend.app.classifier import QueryClassifier
from backend.app.evidence import EvidenceBuilder
from backend.app.rag import RAGPipeline

# ─── 1. Structured Logging ────────────────────────────────────────────────────
import sys

log_file = r"d:\Siddha_Wisdom\backend_run.log"
log_format = "%(asctime)s [%(levelname)s] %(name)s rid=%(request_id)s: %(message)s" \
    if not settings.structured_logging \
    else '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","rid":"%(request_id)s","msg":"%(message)s"}'

class RequestIDFilter(logging.Filter):
    """Injects a per-request ID into every log record."""
    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "startup"
        return True

logging.basicConfig(
    level=logging.getLevelName(settings.log_level),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding="utf-8")
    ]
)
for handler in logging.root.handlers:
    handler.addFilter(RequestIDFilter())

logger = logging.getLogger("siddhaverse_api")

# ─── 2. Rate Limiter (in-memory, per-IP sliding window) ──────────────────────
_rate_counters: Dict[str, list] = defaultdict(list)

def check_rate_limit(client_ip: str) -> bool:
    """Returns True if request is allowed, False if rate-limited."""
    if not settings.rate_limit_enabled:
        return True
    now = time.time()
    window = settings.rate_limit_window_seconds
    requests = _rate_counters[client_ip]
    # Prune old timestamps outside the window
    _rate_counters[client_ip] = [t for t in requests if now - t < window]
    if len(_rate_counters[client_ip]) >= settings.rate_limit_requests:
        return False
    _rate_counters[client_ip].append(now)
    return True

# ─── 3. FastAPI App ───────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup + shutdown lifecycle handler."""
    # Startup
    logger.info(f"SiddhaVerse API starting — env={settings.environment} v1.1.0")
    try:
        repo = SQLiteDocumentRepository()
        cols = repo.list_collections()
        doc_count = cols.get("total_documents", 0)
        logger.info(f"Startup validation OK — {doc_count} documents in corpus")
    except Exception as e:
        logger.error(f"STARTUP VALIDATION FAILED: {e}")
    yield
    # Shutdown
    logger.info("SiddhaVerse API shutting down")

app = FastAPI(
    lifespan=lifespan,
    title="SiddhaVerse API",
    description=(
        "## SiddhaVerse Scholarly Search & RAG API\n\n"
        "A citation-constrained, zero-hallucination AI retrieval API for the Siddha medical corpus.\n\n"
        "### Features\n"
        "- **Lexical Search** (FTS5 BM25) — Tamil, Romanized, English\n"
        "- **Semantic Search** (Qdrant dense embeddings)\n"
        "- **Hybrid Search** (70% Lexical + 30% Vector + RRF)\n"
        "- **Citation-Constrained RAG** (Gemini 1.5 Pro + local simulator)\n"
        "- **Intent Classification** (9 categories, out-of-scope routing)\n\n"
        "### Citation Schema\n"
        "Every RAG answer includes inline `<cite doc=... hash=... />` tags verified against SHA-256 content hashes.\n\n"
        "### Rate Limits\n"
        f"Default: **{settings.rate_limit_requests} requests / {settings.rate_limit_window_seconds}s** per IP."
    ),
    version="1.1.0",
    contact={"name": "SiddhaVerse Team"},
    license_info={"name": "Public Domain Corpus — All Rights Reserved for Software"},
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ─── 4. CORS ─────────────────────────────────────────────────────────────────
origins = [o.strip() for o in settings.allowed_origins.split(",")] \
    if settings.allowed_origins != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ─── 5. Request ID & Logging Middleware ──────────────────────────────────────
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = request.headers.get(settings.request_id_header) or str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    request.state.start_time = time.time()

    # Inject request_id into root logger context via a filter
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.request_id = request_id
        return record
    logging.setLogRecordFactory(record_factory)

    client_ip = request.client.host if request.client else "unknown"

    # Rate limit check
    if not check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded: ip={client_ip}")
        return JSONResponse(
            status_code=429,
            content={"status": "error", "message": "Rate limit exceeded. Please slow down."},
            headers={settings.request_id_header: request_id}
        )

    response: Response = await call_next(request)
    duration_ms = int((time.time() - request.state.start_time) * 1000)
    response.headers[settings.request_id_header] = request_id
    response.headers["X-Response-Time-Ms"] = str(duration_ms)
    logger.info(f"method={request.method} path={request.url.path} status={response.status_code} duration_ms={duration_ms} ip={client_ip}")
    return response

# ─── 6. Dependency Injection (continued) ─────────────────────────────────────

# ─── 7. Dependency Injection ─────────────────────────────────────────────────
query_classifier = QueryClassifier()
evidence_builder = EvidenceBuilder()

def get_repository() -> BaseDocumentRepository:
    if settings.db_type == "sqlite":
        return SQLiteDocumentRepository()
    from backend.app.repositories import PostgresDocumentRepository
    return PostgresDocumentRepository()

def create_envelope(data: Any, meta: Optional[Dict[str, Any]] = None, status: str = "success") -> Dict[str, Any]:
    envelope = {
        "status": status,
        "version": "1.1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data
    }
    if meta:
        envelope["meta"] = meta
    return envelope

# ─── 8. Health & Readiness ───────────────────────────────────────────────────
@app.get(
    "/health",
    tags=["Observability"],
    summary="Liveness probe",
    response_description="Returns 200 if the process is alive."
)
@app.get("/api/v1/health", tags=["Observability"], include_in_schema=False)
def health_check(repo: BaseDocumentRepository = Depends(get_repository)):
    """Kubernetes/Docker liveness probe. Returns service status and DB connectivity."""
    t0 = time.time()
    try:
        collections = repo.list_collections()
        db_ok = True
        doc_count = collections.get("total_documents", 0)
    except Exception as e:
        logger.error(f"Health check DB error: {e}")
        db_ok = False
        doc_count = 0
    latency_ms = int((time.time() - t0) * 1000)
    return create_envelope({
        "status": "healthy" if db_ok else "unhealthy",
        "database_connected": db_ok,
        "document_count": doc_count,
        "environment": settings.environment,
        "version": "1.1.0",
        "latency_ms": latency_ms
    })


@app.get(
    "/ready",
    tags=["Observability"],
    summary="Readiness probe",
    response_description="Returns 200 when the API is ready to serve traffic."
)
def readiness_check(repo: BaseDocumentRepository = Depends(get_repository)):
    """Kubernetes readiness probe. Returns 503 if the database is not reachable."""
    try:
        cols = repo.list_collections()
        doc_count = cols.get("total_documents", 0)
        if doc_count == 0:
            raise HTTPException(status_code=503, detail="Corpus not loaded.")
        return create_envelope({"ready": True, "document_count": doc_count})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service not ready: {e}")


# ─── 9. Search Endpoint ───────────────────────────────────────────────────────
@app.get(
    "/api/v1/search",
    tags=["Search"],
    summary="Multi-mode search",
    response_description="Paginated search results with intent classification and evidence package."
)
def search(
    q: Optional[str] = Query(None, description="Search query string (Tamil, Romanized, or English)"),
    mode: str = Query("lexical", description="Search mode: `lexical` | `vector` | `hybrid`"),
    doc_type: str = Query("all", description="Filter: `verse` | `biography` | `plant` | `formulation` | `manuscript` | `research`"),
    work: str = Query("all", description="Filter by source work: `Thirumandiram` | `Sivavakkiyam`"),
    author: str = Query("all", description="Filter by author name"),
    entity: Optional[str] = Query(None, description="Filter by entity ID (e.g. `plant_tulsi`)"),
    category: Optional[str] = Query(None, description="Filter by entity category"),
    confidence: str = Query("all", description="Entity confidence: `confirmed` | `probable` | `candidate`"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    per_page: int = Query(20, ge=1, le=100, description="Results per page (max 100)"),
    sort: str = Query("relevance", description="Sort: `relevance` | `verse_number` | `work` | `author`"),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """
    Multi-mode search across the 1,174-document Siddha corpus.

    - **lexical**: FTS5 BM25 with Tamil suffix stripping and English synonym expansion
    - **vector**: Dense embedding search (multilingual-e5-large, 1024-dim)
    - **hybrid**: Weighted RRF fusion (70% lexical + 30% vector) with optional cross-encoder reranking
    """
    t0 = time.time()
    query_str = q or ""
    intent = query_classifier.classify(query_str)
    category_intent = intent.get("category")

    if category_intent == "out_of_scope":
        logger.info(f"Out-of-scope: '{query_str}'")
        return create_envelope(
            {"query": query_str, "results": [], "message": "The query falls outside the scope of the SiddhaVerse library."},
            meta={"total": 0, "page": page, "per_page": per_page, "total_pages": 0,
                  "query_time_ms": int((time.time() - t0) * 1000), "intent": intent}
        )

    if category_intent == "greeting":
        return create_envelope(
            {"query": query_str, "results": [],
             "message": "Greetings! I am the SiddhaVerse Scholarly Retrieval Assistant. How can I help you explore the texts today?"},
            meta={"total": 0, "page": page, "per_page": per_page, "total_pages": 0,
                  "query_time_ms": int((time.time() - t0) * 1000), "intent": intent}
        )

    if mode == "vector":
        results, total = repo.search_vector(q=query_str, doc_type=doc_type, work=work, author=author,
                                            entity_id=entity, page=page, per_page=per_page)
    elif mode == "hybrid":
        results, total = repo.search_hybrid(q=query_str, doc_type=doc_type, work=work, author=author,
                                            entity_id=entity, page=page, per_page=per_page)
    else:
        results, total = repo.search_lexical(q=query_str, doc_type=doc_type, work=work, author=author,
                                             entity_id=entity, category=category, page=page,
                                             per_page=per_page, sort=sort)

    evidence_package = {}
    if results:
        evidence_package = evidence_builder.build_evidence_package(results)

    latency_ms = int((time.time() - t0) * 1000)
    formatted_results = [
        {
            "document_id": doc.get("document_id"),
            "title": doc.get("title"),
            "source_work": doc.get("source_work"),
            "author": doc.get("author"),
            "collection": doc.get("collection"),
            "verse_number": doc.get("verse_number"),
            "doc_type": doc.get("doc_type"),
            "tamil_text": doc.get("tamil_text"),
            "transliteration": doc.get("transliteration"),
            "entity_ids": doc.get("entity_ids"),
            "source_url": doc.get("source_url"),
            "snippet": (doc.get("tamil_text") or doc.get("search_text", ""))[:150] + "..."
        }
        for doc in results
    ]
    return create_envelope(
        {"query": query_str, "results": formatted_results},
        meta={"total": total, "page": page, "per_page": per_page,
              "total_pages": (total + per_page - 1) // per_page,
              "query_time_ms": latency_ms, "intent": intent,
              "evidence_package": evidence_package.get("context_package")}
    )


# ─── 10. Lookup Endpoints ─────────────────────────────────────────────────────
@app.get("/api/v1/verse/random", tags=["Corpus"], summary="Random verse")
def get_random_verse(
    work: str = Query("all", description="Limit to source work"),
    entity: Optional[str] = Query(None, description="Limit by entity_id"),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """Returns a random verse document, optionally filtered by work or entity."""
    verse = repo.get_random_verse(work=work, entity_id=entity)
    if not verse:
        raise HTTPException(status_code=404, detail="No matching verse found.")
    return create_envelope(verse)


@app.get("/api/v1/verse/{id}", tags=["Corpus"], summary="Verse by ID")
def get_verse(
    id: str = Path(..., description="Document ID, e.g. `thirumandiram_pm_0127`"),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """Retrieve a single classical verse by document ID."""
    verse = repo.get_document_by_id(id)
    if not verse or verse.get("doc_type") != "verse":
        raise HTTPException(status_code=404, detail=f"Verse '{id}' not found.")
    return create_envelope(verse)


@app.get("/api/v1/entity/{id}", tags=["Corpus"], summary="Entity by ID")
def get_entity(
    id: str = Path(..., description="Entity ID, e.g. `plant_tulsi`"),
    include_verses: bool = Query(False, description="Include linked verse IDs"),
    include_crossrefs: bool = Query(False, description="Include co-occurring entities"),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """Retrieve entity metadata, optionally with verse links and cross-references."""
    ent = repo.get_entity_by_id(id)
    if not ent:
        raise HTTPException(status_code=404, detail=f"Entity '{id}' not found.")
    if not include_verses:
        ent.pop("sample_verse_ids", None)
    if not include_crossrefs:
        ent.pop("co_occurring_entities", None)
    return create_envelope(ent)


@app.get("/api/v1/plant/{id}", tags=["Corpus"], summary="Medicinal plant by ID")
def get_plant(
    id: str = Path(..., description="Plant document ID, e.g. `plant_nilavembu`"),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """Retrieve a medicinal plant profile from the Siddha Materia Medica."""
    plant = repo.get_plant_by_id(id)
    if not plant:
        raise HTTPException(status_code=404, detail=f"Plant '{id}' not found.")
    return create_envelope(plant)


@app.get("/api/v1/siddhar/{id}", tags=["Corpus"], summary="Siddhar biography by ID")
def get_siddhar(
    id: str = Path(..., description="Siddhar document ID, e.g. `siddhar_thirumoolar`"),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """Retrieve a Siddhar biography profile."""
    bio = repo.get_siddhar_by_id(id)
    if not bio:
        raise HTTPException(status_code=404, detail=f"Siddhar '{id}' not found.")
    return create_envelope(bio)


@app.get("/api/v1/work/{id}", tags=["Corpus"], summary="Classical work index")
def get_work(
    id: str = Path(..., description="Work ID: `thirumandiram` | `sivavakkiyam`"),
    collection: str = Query("all", description="Filter by collection / tantiram"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """Retrieve the verse index for a classical work, paginated."""
    work = repo.get_work_by_id(id, collection=collection, page=page, per_page=per_page)
    if not work:
        raise HTTPException(status_code=404, detail=f"Work '{id}' not found.")
    meta = {
        "total": work["total_verses_in_corpus"],
        "page": page, "per_page": per_page,
        "total_pages": (work["total_verses_in_corpus"] + per_page - 1) // per_page
    }
    return create_envelope(work, meta=meta)


@app.get("/api/v1/formulation/{id}", tags=["Corpus"], summary="Formulation by ID")
def get_formulation(
    id: str = Path(..., description="Formulation ID, e.g. `formulation_kabasura_kudineer`"),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """Retrieve a Siddha medicine formulation with ingredients and preparation method."""
    form = repo.get_formulation_by_id(id)
    if not form:
        raise HTTPException(status_code=404, detail=f"Formulation '{id}' not found.")
    return create_envelope(form)


@app.get("/api/v1/collections", tags=["Corpus"], summary="Corpus index")
def list_collections(repo: BaseDocumentRepository = Depends(get_repository)):
    """List all navigable works, entity categories, and document type counts."""
    return create_envelope(repo.list_collections())


# ─── 11. RAG Endpoints ────────────────────────────────────────────────────────
@app.get(
    "/api/v1/rag",
    tags=["RAG"],
    summary="Citation-constrained RAG (GET)",
    response_description="Fact-verified answer with inline citations."
)
def rag_ask_get(
    q: str = Query(..., description="Natural language question about Siddha medicine or philosophy"),
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """
    Ask a question to the citation-constrained RAG system.

    Every statement in the answer is backed by a verified corpus document.
    Unsupported queries are refused gracefully — no hallucination is possible.

    **Citation format**: `<cite doc="document_id" hash="sha256_hash" />`

    **Refusal triggers**:
    - Query out of scope
    - No lexical match + low vector confidence (< 0.82)
    - No high-confidence results (score < 0.55)
    - Citation hash mismatch (hallucination detected)
    """
    pipeline = RAGPipeline(repo)
    result = pipeline.run(q)
    return create_envelope(result)


class RAGRequest(BaseModel):
    query: str

    model_config = {"json_schema_extra": {"example": {"query": "What is Kayakalpa in Siddha medicine?"}}}


@app.post(
    "/api/v1/rag",
    tags=["RAG"],
    summary="Citation-constrained RAG (POST)",
    response_description="Fact-verified answer with inline citations."
)
def rag_ask_post(
    req: RAGRequest,
    repo: BaseDocumentRepository = Depends(get_repository)
):
    """
    Ask a question to the citation-constrained RAG system via JSON body.

    See GET /api/v1/rag for full documentation.
    """
    pipeline = RAGPipeline(repo)
    result = pipeline.run(req.query)
    return create_envelope(result)
