# Test Results — SiddhaVerse

This document presents the detailed results of executing the complete test suite for the search and retrieval backend (Phase 3A).

## Executive Summary

- **Total Tests Run:** 15
- **Passed:** 15 (100%)
- **Failed:** 0 (0%)
- **Warnings:** 2
- **Execution Time:** 0.60 seconds
- **Platform:** Windows (Python 3.14.4)
- **Status:** **ALL PASSED**

## Detailed Test Suite Breakdown

### 1. API Endpoints Suite (`backend/tests/test_api.py`)
Verifies HTTP endpoints against the FastAPI `TestClient` matching the canonical API contract.

| Test Name | Focus Area | Status |
| :--- | :--- | :--- |
| `test_api_health` | FastAPI health check, database connectivity | PASSED |
| `test_api_search_success` | Lexical search success | PASSED |
| `test_api_search_greeting` | Greeting query routing and intent detection | PASSED |
| `test_api_search_out_of_scope` | Out of scope intent handling | PASSED |
| `test_api_get_verse` | Retrieval of single verse by ID | PASSED |
| `test_api_get_verse_not_found` | Verse not found handling (404 error) | PASSED |
| `test_api_get_entity` | Entity lookup, filters for verse IDs & cross-refs | PASSED |
| `test_api_get_plant` | Retrieval of medicinal plant profile | PASSED |
| `test_api_get_siddhar` | Retrieval of Siddhar biography profile | PASSED |
| `test_api_get_work` | Retrieval of metadata & index for a work (Thirumandiram) | PASSED |
| `test_api_get_formulation` | Retrieval of formulation recipe profile | PASSED |
| `test_api_list_collections` | Listing navigable works and categories | PASSED |

### 2. Component Core Suite (`backend/tests/test_components.py`)
Validates individual python class logic for classifier, evidence builder, and repositories.

| Test Name | Focus Area | Status |
| :--- | :--- | :--- |
| `test_query_classifier` | Classifying intents: greetings, out of scope, philosophy, plants, places, etc. | PASSED |
| `test_evidence_builder` | Context deduplication, token limiting, template output | PASSED |
| `test_repository_getters` | Database query helper logic: random verse, specific entities, plants, Siddhars, adjacent verses | PASSED |

## Warnings Summary
1. `StarletteDeprecationWarning`: `testclient` httpx deprecation (minor third-party dependency warning).
2. `PydanticDeprecatedSince20`: Class-based config deprecation in `config.py` (to be updated to `ConfigDict` in upcoming revision).
