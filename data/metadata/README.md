# Dataset Metadata & Audit Catalogues (`data/metadata/`)

This directory contains lightweight, machine-readable metadata records, data schemas, verification logs, and catalogues describing the research datasets used across all five phases.

## Current Files

- **`dataset_inventory.csv`**: The central project-wide dataset catalogue listing all 27 candidate datasets across 6 categories with official URLs, variables needed, resolution, access requirements, and project priorities (Required vs. Optional vs. Reference).
- **`regional_availability_matrix.csv`**: Regional assessment matrix documenting empirical availability across Bengaluru, Mysuru, and Nilgiri–Bandipur.
- **`osm_reference_boundaries_metadata.json`**: Provenance metadata for raw OpenStreetMap reference boundaries stored in `data/raw/osm_reference_boundaries/`.
- **`phase_1_checks/`**: Empirical verification tables from Phase 1 notebooks:
  - `window_reference_feature_coverage.csv`: Percentage of each OSM reference feature inside its designated study window.
  - `official_url_checks.csv`: Results of live HTTP probes against all official URLs.
  - `gbif_regional_summary.csv`: Empirical count of GBIF records and 1992–2013 vs 2014–2024 split.
  - `inaturalist_regional_summary.csv`: Empirical count of research-grade observations.
  - `osm_highway_lit_summary.csv`: Audit of road network length and `lit=*` street lighting completeness.
  - `raster_tile_verification.csv`: Verification of public cloud raster tile existence (Copernicus DEM S3, Hansen GFC).

Unlike raw raster and bulk observation files, files in this directory are tracked in Git to maintain scientific traceability.

