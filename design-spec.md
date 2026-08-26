# Multimodal Agent Builder — Design Spec


> **IMMUTABLE BASELINE** — Do not rewrite this document.
> Policy: `Structure/spec-immutability/` · Enforce: `python3 Structure/spec-immutability/scripts/check_specs.py`
> Changes after seal: **amend only** under `## Amendments` (append). Never replace the body above `<!-- SPEC-BASELINE-END -->`.

## Architecture
- **Client:** React/TSX app under `client/`
- **Server:** TypeScript/Python services under `server/` and `src/`
- **Shared schema:** `shared/schema.ts`
- **Config:** `config/config.py`
- **Examples & scripts:** `examples/`, `scripts/`

## Design principles
1. Provider adapters behind one agent abstraction.
2. Multimodal pipelines as first-class inputs, not bolt-ons.
3. Explicit train/test/validate closure ledgers for agent quality.

<!-- SPEC-BASELINE-END -->

## Amendments

_No amendments yet. Append new entries below this line only. Do not edit the baseline above the marker._
