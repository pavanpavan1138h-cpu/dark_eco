# Scripts Directory (`scripts/`)

This directory contains standalone Python support modules, command-line utilities, and validation tools used by the Jupyter notebooks.

## Subdirectories

- **`utilities/`**:
  - `dei_paths.py`: Project-relative path resolver ensuring notebooks never use hardcoded absolute personal paths.
  - `dei_geo.py`: Geodetic transformation module (WGS 84 to UTM Zone 43N) and 5 km × 5 km spatial grid builder.
  - `dei_http.py`: Rate-limited, polite HTTP request wrappers with retries and sha256 checksum generators.
- **`validation/`**:
  - QA/QC check scripts for data integrity, missing-value auditing, and boundary compliance.
- **`phase_1_setup/`**:
  - Initial setup scripts authored during Phase 1 (`generate_boundaries_and_grids.py`, `generate_inventory_and_matrix.py`).

All scripts adhere to PEP 8 standards, contain descriptive docstrings, and handle errors transparently.

