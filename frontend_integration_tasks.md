# SiddhaVerse Frontend Integration Tasks

---

## M1 — Search Integration
**Goal**: Wire the existing search bar to `GET /api/v1/search` and render results.

| Field | Detail |
|---|---|
| **Files** | `index.html` |
| **APIs** | `GET /api/v1/search?q=&mode=lexical&page=&per_page=` |
| **Success Criteria** | Typing in the search bar fires the API; results appear as cards below the hero; pagination works; empty/OOD queries show graceful message |
| **Complexity** | Low |

---

## M2 — Verse of the Day
**Goal**: Replace static/placeholder content with a live random verse on page load.

| Field | Detail |
|---|---|
| **Files** | `index.html` |
| **APIs** | `GET /api/v1/verse/random` |
| **Success Criteria** | On load, a verse card renders with Tamil text, transliteration, source work, and verse number; refreshes each page load |
| **Complexity** | Low |

---

## M3 — Explore Cards (Collections Index)
**Goal**: Populate Works, Siddhars, Plants, and Formulations browse sections from live data.

| Field | Detail |
|---|---|
| **Files** | `index.html` |
| **APIs** | `GET /api/v1/collections` |
| **Success Criteria** | Each category card shows real document counts; clicking a card triggers a filtered search (`doc_type=plant`, `doc_type=biography`, etc.) |
| **Complexity** | Low |

---

## M4 — Document Viewer (Detail Panel)
**Goal**: Clicking any result card opens a full document detail view without a page reload.

| Field | Detail |
|---|---|
| **Files** | `index.html` |
| **APIs** | `GET /api/v1/verse/{id}`, `GET /api/v1/entity/{id}`, `GET /api/v1/plant/{id}`, `GET /api/v1/siddhar/{id}`, `GET /api/v1/formulation/{id}` |
| **Success Criteria** | A slide-in panel or modal renders full document fields (Tamil, transliteration, entities, source URL); browser back button closes the panel; direct URL hash links to document |
| **Complexity** | Medium |

---

## M5 — Search Mode Switcher (Hybrid / Semantic)
**Goal**: Expose `mode=lexical | hybrid | vector` toggle in the UI.

| Field | Detail |
|---|---|
| **Files** | `index.html` |
| **APIs** | `GET /api/v1/search?mode=hybrid` |
| **Success Criteria** | Three-button mode selector visible; selected mode passed in query; results update; active mode visually distinguished |
| **Complexity** | Low |

---

## M6 — AI Ask Panel (Planning Only — No LLM Key Required)
**Goal**: Add a visible AI Ask input that calls the RAG endpoint; gracefully handles simulator mode.

| Field | Detail |
|---|---|
| **Files** | `index.html` |
| **APIs** | `POST /api/v1/rag` `{"query":"..."}` |
| **Success Criteria** | Input box + Submit button present; response answer rendered with inline citations; refused/unsupported queries show refusal message; loading spinner during request |
| **Complexity** | Medium |

---

## M7 — Health Status Indicator
**Goal**: Show a live API status badge in the UI header.

| Field | Detail |
|---|---|
| **Files** | `index.html` |
| **APIs** | `GET /health` |
| **Success Criteria** | Badge shows "Online" (green) when healthy, "Offline" (red) when unreachable; checked on page load |
| **Complexity** | Low |

---

## M8 — Backend Deployment (Docker)
**Goal**: Run the FastAPI backend in production mode accessible to the frontend.

| Field | Detail |
|---|---|
| **Files** | `Dockerfile`, `docker-compose.yml`, `.env.production` |
| **APIs** | All |
| **Success Criteria** | `docker-compose up -d` starts the API; `/health` returns `"status":"healthy"`; `/ready` returns `"ready":true`; `index.html` served from same origin or configured CORS |
| **Complexity** | Medium |

---

## M9 — Frontend Deployment
**Goal**: Serve `index.html` as a static file via the FastAPI backend or a static host.

| Field | Detail |
|---|---|
| **Files** | `index.html`, `backend/app/main.py` |
| **APIs** | `StaticFiles` mount or external CDN |
| **Success Criteria** | Navigating to `http://host/` loads the frontend; all API calls resolve without CORS errors; `ALLOWED_ORIGINS` set correctly in `.env.production` |
| **Complexity** | Low |

---

## Milestone Sequence

```
M7 (Health)
  → M1 (Search)
    → M2 (Verse of Day)
    → M3 (Explore Cards)
      → M4 (Document Viewer)
        → M5 (Mode Switcher)
          → M6 (AI Ask)
            → M8 (Backend Deploy)
              → M9 (Frontend Deploy)
```
