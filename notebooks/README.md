# Notebooks Directory (`notebooks/`)

This directory houses all Jupyter Notebook workflows (`.ipynb`) for the Dark Ecology Intelligence (DEI) project. In accordance with project instructions, all five project phases are implemented primarily through executable, beginner-friendly notebooks.

## Structure by Phase

- **`Phase_1_Setup.ipynb`**: Consolidated master setup notebook for Phase 1.
- **`phase_1_setup/`**:
  - `01_project_and_geographical_setup.ipynb`: Boundaries, metric UTM 43N CRS, and 5 km × 5 km regular grid generation.
  - `02_dataset_source_investigation.ipynb`: Central dataset catalogue, official URLs, access checks, and temporal profile analysis.
  - `03_regional_availability_assessment.ipynb`: Live empirical API probes (GBIF, iNaturalist, Overpass, AWS S3) and regional availability matrix.
- **`phase_2_nighttime_lights/`**: Nighttime light ingestion (DMSP-OLS, VIIRS-DNB, Black Marble, harmonised series).
- **`phase_3_biodiversity/`**: Occurrence ingestion, citizen science filtering, and occupancy modelling (GBIF, eBird, iNaturalist).
- **`phase_4_foodweb_traits/`**: Trophic interaction networks (GloBI) and functional traits (EltonTraits, AVONET, PanTHERIA).
- **`phase_5_environmental_data/`**: Land cover (ESA WorldCover), forest loss (Hansen GFC), DEM, population (WorldPop), and climate (ERA5-Land).

## Execution Standards

- Every notebook uses project-relative paths via `scripts/utilities/dei_paths.py`.
- No notebook generates or uses synthetic data.
- Executed outputs and visualizations are preserved in the repository.

