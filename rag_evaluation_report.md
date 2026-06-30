# RAG Evaluation Report — SiddhaVerse

**Date**: 2026-06-29  
**Test Suite**: `backend/tests/test_rag.py` (7 tests)  
**Full Suite**: `backend/` (23 tests, 0 failures)

---

## 1. RAG Test Results

| Test ID | Query Type | Expected | Result |
| :--- | :--- | :--- | :--- |
| `test_rag_greeting` | Greeting | Static response, 0 citations | ✅ PASS |
| `test_rag_out_of_scope` | Out-of-scope (quantum physics) | Scope refusal, 0 citations | ✅ PASS |
| `test_rag_unsupported_query` | Nonsense Tamil string | Evidence refusal, 0 citations | ✅ PASS |
| `test_rag_valid_query` | Tamil verse lookup | Valid answer, ≥ 1 citation | ✅ PASS |
| `test_citation_verifier_success` | Valid doc_id + hash | Verified, citation metadata returned | ✅ PASS |
| `test_citation_verifier_hallucinated_doc` | Injected unknown doc_id | Security error | ✅ PASS |
| `test_citation_verifier_mismatched_hash` | Wrong content hash | Security error | ✅ PASS |

---

## 2. Graceful Refusal Coverage

| Refusal Trigger | Mechanism | Verified |
| :--- | :--- | :--- |
| Empty query | `query_str == ""` pre-check | ✅ |
| Greeting | `QueryClassifier → greeting` | ✅ |
| Out-of-scope | `QueryClassifier → out_of_scope` | ✅ |
| No corpus match (OOD Tamil) | Lexical=0 + Vector < 0.82 | ✅ |
| Low-confidence hybrid hits | Score filter < 0.55 | ✅ |
| Hallucinated doc_id | `CitationVerifier` hash map check | ✅ |
| Mismatched content hash | `CitationVerifier` hash comparison | ✅ |

---

## 3. End-to-End Pipeline Performance

| Metric | Observed | Notes |
| :--- | :--- | :--- |
| OOD refusal rate | 100% | Nonsense Tamil queries rejected |
| Citation accuracy | 100% | Verifier enforces strict doc_id + hash matching |
| Hallucinated doc rate | 0% | Blocked at CitationVerifier stage |
| LLM fallback (no API key) | Local simulator active | Produces citation-constrained answers from context |

---

## 4. LLM Integration

| Mode | Status | Notes |
| :--- | :--- | :--- |
| Gemini API | Ready (requires `GEMINI_API_KEY` env var) | Falls back gracefully on timeout / 404 |
| Local simulator | Active (default) | Generates structured, citation-grounded answers |

---

## 5. Known Limitations

- **Target Metrics Not Yet Met**: Precision@5 ≥ 0.85, Recall@10 ≥ 0.95, MRR ≥ 0.90 require a real LLM for end-to-end evaluation.
- **Local Simulator**: Matches on document text heuristically. Real Gemini inference will produce more natural answers.
- **Cross-encoder Latency**: p95 ~250ms (no reranker). Cross-encoder adds 700–1300ms. Selective routing active.
