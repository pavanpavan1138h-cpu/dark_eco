# Data Directory (`data/`)

This directory is the root storage for all project datasets. In strict adherence to scientific data integrity and reproducibility principles, this directory maintains a three-way architectural separation:

- **`raw/`**: Immutable raw data archives downloaded from original sources.
- **`processed/`**: Cleaned, transformed, and gridded spatial-temporal feature arrays.
- **`metadata/`**: Machine-readable data catalogues, STAC records, schemas, and verification logs.
- **`external_references/`**: Non-tabular reference files, documentation PDFs, and institutional reports.

## Strict Data Integrity Protocols
1. **NO SYNTHETIC DATA**: No simulated, fabricated, or pseudo-random records exist anywhere in these folders.
2. **IMMUTABILITY**: Files in `raw/` are never overwritten, edited, or manually cleaned. All cleaning and transformation happens reproducibly via code into `processed/`.
3. **GIT EXCLUSION**: All large raster files (*.tif, *.nc, *.h5, *.grib), parquet tables, shapefiles, and large CSVs are strictly excluded from version control via `.gitignore`.

