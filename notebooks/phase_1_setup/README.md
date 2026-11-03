# Phase 1 Setup Notebooks (`notebooks/phase_1_setup/`)

This directory contains the executable Jupyter notebooks for **Phase 1: Research Setup, Geographical Definition, and Dataset Source Inventory**.

## Notebooks

1. **`01_project_and_geographical_setup.ipynb`**:
   - Delineates the three 50 km × 50 km study windows (Bengaluru, Mysuru, Nilgiri–Bandipur) in UTM Zone 43N (`EPSG:32643`).
   - Generates the 300 regular 5 km × 5 km grid cells ($25\text{ km}^2$ each) and exports GeoJSON files to `geographical_boundaries/`.
   - Cross-checks window contents against real OpenStreetMap reference polygons (BBMP, Bannerghatta, Ranganathittu, Bandipur, Mudumalai).
   - Conducts sensitivity analysis on shifting the Nilgiri–Bandipur window to maximise protected area coverage.

2. **`02_dataset_source_investigation.ipynb`**:
   - Establishes the project-wide central dataset inventory across 6 categories (ALAN, Biodiversity, Food Webs, Traits, Environment, Validation).
   - Executes live HTTP health checks against all official data portal URLs.
   - Maps documented temporal coverage across the 1992–2024 target window.
   - Applies the "Collect only necessary data" rule to classify datasets into *Required*, *Optional*, and *Reference only*.

3. **`03_regional_availability_assessment.ipynb`**:
   - Executes non-destructive empirical API probes across our three study windows.
   - Measures real GBIF and iNaturalist record volumes, proving the post-2014 citizen science surge.
   - Audits OpenStreetMap road network and street lighting (`lit=*`) completeness via Overpass API.
   - Confirms public cloud raster tile existence (Copernicus DEM on AWS S3, Hansen GFC on Google Cloud Storage).
   - Compiles and exports the official `regional_availability_matrix.csv`.

