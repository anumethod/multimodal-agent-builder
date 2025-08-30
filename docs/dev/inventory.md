# Developer Inventory: multimodal-agent-builder

This document provides a quick reference for all major workflows, scripts, entry points, and developer automation present in the repository.

## Data Reassembly

- **Script:** `scripts/reassemble_files.sh`
- **Usage:**
  - `bash scripts/reassemble_files.sh` (standard)
  - `bash scripts/reassemble_files.sh --kind testing` (after parameterization)
  - Aids in reconstructing split datasets for ML train/test/validation.

## Model Training

- **Main training module:** (To be filled: likely in `src/agents/`, `src/models/`, or similar)
- **Entry-point(s):** (`train()` or CLI script; please fill exact file/function on next audit)
- **Ledger integration planned/underway:** See training loop functions.

## Testing & Automation

- **Test scripts:** `tests/`
- **Sample test:** `pytest`
- **Reassembly verification:** Planned as `tests/reassembly/test_matrix.py`
- **Ledger test:** Planned as `tests/ledger/test_recursive_closure.py`

## Code Quality & Linting

- **Formatting:** `ruff format .` (Python)
- **Lint:** `ruff check --select ALL --ignore I001 .`
- **Typechecking:** `mypy --strict .`
- **JS/TS format/lint:** `npm run prettier` and `npm run lint:fix`

## Developer Automation

- **Hooks:** See `.pre-commit-config.yaml`
- **Pipeline:** See `.github/workflows/ci.yaml`

---

_Update this doc as new scripts, pipelines, or workflow files are added._
