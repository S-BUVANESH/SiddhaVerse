# Dependency Versions — SiddhaVerse

This document lists the verified dependency versions for the SiddhaVerse search infrastructure as of the implementation of Phase 3A.

## Python Interpreter
- **Version:** Python 3.14.4 (win32)

## Python Packages

| Package Name | Installed Version | Requirement | Status |
| :--- | :--- | :--- | :--- |
| `fastapi` | **0.138.1** | `fastapi` | Verified |
| `pydantic` | **2.12.4** | `pydantic` | Verified |
| `pydantic-settings` | **2.14.2** | `pydantic-settings` | Verified |
| `sqlalchemy` | **2.0.51** | `sqlalchemy` | Verified |
| `pytest` | **9.1.1** | `pytest` | Verified |
| `requests` | **2.32.5** | `requests` | Verified |

## Verification Details
- **Verification Method:** Programmatic import and version query (`__version__`) executed via terminal.
- **Verification Timestamp:** 2026-06-25 16:31:24 UTC
