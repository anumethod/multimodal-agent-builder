# Multimodal Agent Builder — Technical Spec


> **IMMUTABLE BASELINE** — Do not rewrite this document.
> Policy: `Structure/spec-immutability/` · Enforce: `python3 Structure/spec-immutability/scripts/check_specs.py`
> Changes after seal: **amend only** under `## Amendments` (append). Never replace the body above `<!-- SPEC-BASELINE-END -->`.

## Stack
- Backend: FastAPI / Python (`src/`, `run.py`)
- Frontend: React + Vite/TS (`client/`)
- DB schema: Drizzle (`drizzle.config.ts`)
- Tests: pytest (`tests/`, `run_tests.py`)
- Packaging: `pyproject.toml`, `package.json`

## Key APIs
Agent create/run/manage endpoints (see README and `docs/`).

## Out of scope
Return42 mesh/SIP hardware validation.

<!-- SPEC-BASELINE-END -->

## Amendments

_No amendments yet. Append new entries below this line only. Do not edit the baseline above the marker._
