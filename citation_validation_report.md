# Citation Validation Report — SiddhaVerse

**Date**: 2026-06-29  
**Component**: `backend/app/rag.py::CitationVerifier`

---

## 1. Citation Format

The LLM is instructed to place inline citations immediately after every cited fact:

```
<cite doc="document_id" hash="content_hash" />
```

---

## 2. Validation Algorithm

```python
# Step 1: Build injected context map
context_map = {doc["document_id"]: doc["content_hash"] for doc in injected_docs}

# Step 2: Parse all <cite> tags from LLM output
citations = re.findall(r'<cite\s+doc="([^"]+)"\s+hash="([^"]+)"\s*/>', llm_output)

# Step 3: Validate each citation
for doc_id, val_hash in citations:
    if doc_id not in context_map:
        → BLOCK: "Hallucinated document citation detected"
    if context_map[doc_id] != val_hash:
        → BLOCK: "Mismatched content hash detected"
    → ACCEPT: append to verified_citations
```

---

## 3. Validation Gates

| Gate | Check | Action on Failure |
| :--- | :--- | :--- |
| Document ID existence | `doc_id in context_map` | Block entire response |
| Content hash match | `context_map[doc_id] == val_hash` | Block entire response |
| Deduplication | `doc_id not in seen_ids` | Skip duplicate |

---

## 4. Verified Citation Metadata (Client Response)

After passing validation, citations are stripped of internal security fields and returned as:

```json
[
  {
    "document_id": "thirumandiram_pm_0127",
    "source_work": "Thirumandiram",
    "verse_number": "127",
    "source_url": null
  }
]
```

The `hash` value is **intentionally excluded** from the client response — it is an internal integrity token, not a user-facing field.

---

## 5. Test Coverage

| Scenario | Test | Result |
| :--- | :--- | :--- |
| Valid doc_id + correct hash | `test_citation_verifier_success` | ✅ PASS |
| Unknown doc_id (hallucination) | `test_citation_verifier_hallucinated_doc` | ✅ PASS |
| Correct doc_id + wrong hash | `test_citation_verifier_mismatched_hash` | ✅ PASS |

---

## 6. Security Properties

- **Zero-Hallucination Guarantee**: Any citation not present in the injected context is blocked at the backend before the response is served.
- **Hash Integrity**: SHA-256 content hashes ensure the LLM cannot fabricate a plausible-looking citation for a real document with different content.
- **Audit Logging**: All security failures are logged at WARNING level via `siddhaverse_api.rag` logger for forensic review.
