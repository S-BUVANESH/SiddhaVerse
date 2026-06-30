# Technology Decision Report — SiddhaVerse

## Document Information
- **Role**: Lead Systems Architect  
- **System Version**: v3.0-RC1  
- **Target**: Production Architecture Selection  

---

## 1. LLM Model Evaluation & Comparisons

To maintain scholarly integrity and support bilingual retrieval, the LLM must have strong reasoning capabilities, excellent Tamil comprehension, and strict instruction-following performance.

### Comparative Models Matrix:

| Model | Size | Strengths | Weaknesses | Best Fit |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 1.5 Pro** | API | Large context window (2M tokens), industry-leading Tamil translation/understanding, strong citation alignment. | Cloud dependency, latency spikes. | **Cloud (Recommended)** |
| **Gemma 2 27B** | 27B | High performance for open weights, excellent reasoning, compact, easily self-hosted. | Needs GPU local hosting (≥ 24GB VRAM). | **Local / Hybrid (Alternative)** |
| **Llama 3 70B** | 70B | Excellent instruct tuning, broad tool support, robust instruction-following. | High hardware footprint, Tamil coverage is moderate compared to Gemini. | **Cloud Private Hosting** |
| **Qwen 2 7B / 72B**| 7B/72B | Outstanding multilingual capabilities (trained on extensive non-English text). | Complex context handling in edge-case prompts. | **Multilingual Search alternative** |

### Recommendations:
1. **Local Deployment**: **Gemma 2 9B-IT / 27B-IT** (via Ollama / vLLM). Compact enough to run on standard developer workstations or local servers while maintaining robust instruction-following performance for citation tags.
2. **Cloud Deployment**: **Gemini 1.5 Pro** (via Google AI Studio / Vertex AI). Unmatched Tamil-English semantic reasoning and native integration into Google Cloud infrastructure.

---

## 2. Technology Stack Selection

To scale the platform to 100,000+ documents, we recommend a decoupled, service-oriented architecture:

```
+-------------------------------------------------------------+
|                      1. FRONTEND LAYOUT                     |
|           React / Next.js | Tailwind CSS | HSL Theme        |
|             (Deployed on Vercel / Netlify CDN)               |
+-------------------------------------------------------------+
                               |
                               | (HTTPS / REST API)
                               v
+-------------------------------------------------------------+
|                      2. BACKEND LAYER                       |
|           FastAPI (Python) | Uvicorn | Docker Container     |
|                 (Deployed on Render / AWS ECS)              |
+-------------------------------------------------------------+
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
+-----------------------+             +-----------------------+
|   3. METADATA STORE   |             |   4. EMBEDDING STORE  |
| PostgreSQL (JSONB) /  |             |  Qdrant Vector DB     |
|     SQLite (FTS5)     |             |  (Docker Container)   |
+-----------------------+             +-----------------------+
```

### Component Details & Justifications:

#### A. Frontend: React / Next.js (with Vanilla CSS variables)
- **Why**: Static Site Generation (SSG) and Incremental Static Regeneration (ISR) compile search routes and entity pages into static HTML assets. This delivers lightning-fast load times, excellent SEO indexing, and negligible server costs.

#### B. Backend: FastAPI (Python 3.11)
- **Why**: python is the standard for NLP libraries (spaCy, tokenizers) and vector math scripts. FastAPI provides automatic OpenAPI generation, async concurrency, and high-performance routing.

#### C. Search Engine: SQLite FTS5 (Lexical)
- **Why**: Extremely fast, serverless, and stores the full lexical index in a single file database.
- **Scale Plan**: SQLite FTS5 is highly performant up to 5,000–10,000 documents. At 100,000+ documents, we can migrate seamlessly to **PostgreSQL with pg_trgm and FTS**, or a dedicated **MeiliSearch** cluster.

#### D. Vector embedding Database: Qdrant
- **Why**: Written in Rust, has high memory efficiency, and supports hybrid filtering (performing strict SQL metadata pre-filtering on vectors before similarity calculations).
- **Alternative**: Milvus or pgvector (if unified Postgres storage is prioritized).

#### E. Embedding Models: `multilingual-e5-large`
- **Why**: Consistently ranks at the top of the MTEB (Massive Text Embedding Benchmark) for multilingual retrieval, mapping Tamil and English terms into a shared vector space.

---

## 3. Hosting, Scalability, and Costs

| Tier | Component | Hosting Provider | Cost Profile | Scalability Plan |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | Static Assets | Vercel (Free / Pro) | $0 - $20 / month | Global Edge CDN distribution |
| **Backend** | API Services | Render Web Service | $7 / month | Scaled via AWS ECS at 100k+ docs |
| **Database** | SQL Metadata | Render Managed Postgres | $7 / month | Read-replicas |
| **Vector DB**| Vector Index | Qdrant Cloud (Free Tier) | $0 - $19 / month | HNSW indexing clusters |
| **LLM Inference**| Semantic Generation | Google AI Studio | Pay-as-you-go | Distributed Cloud Endpoint |

---

*Report generated by SiddhaVerse Systems Architecture Board, 2026-06-25*
