# Dark Ecology Intelligence (DEI)
**Artificial Neural Networks — Problem-Based Learning (ANN PBL)**

---

## 1. Project Overview

**Dark Ecology Intelligence (DEI)** is an academic research project investigating the multidecadal ecological consequences of Artificial Light at Night (ALAN), land-use transformation, and environmental change across Southern India. 

The research spans three distinct bioclimatic and anthropogenic landscapes:
1. **Bengaluru Urban-Periurban Landscape**: A rapidly growing megacity undergoing massive urbanization, industrialization, and nocturnal light pollution expansion.
2. **Mysuru Peri-Urban & Transitional Landscape**: A historical urban center with intermediate lighting intensity surrounded by an intensive agricultural and riverine matrix (Cauvery and Kabini river basins).
3. **Nilgiri–Bandipur Forest & Ecological Corridor**: A protected tropical dry and moist deciduous forest landscape comprising Bandipur National Park (Karnataka) contiguous with Mudumalai Tiger Reserve (Tamil Nadu) and the Moyar/Sigur elephant corridor, representing a critical biodiversity baseline with localized anthropogenic lighting pressures.

The long-term engineering and modeling objective is to construct **Spatio-Temporal Graph Neural Networks (ST-GNNs)** and formulate **Reinforcement Learning (RL)** policies to simulate nocturnal ecological integrity and evaluate spatial lighting interventions.

---

## 2. Project Directory Structure

All project assets, data pipelines, boundaries, scripts, and reports reside strictly within the `dark_eco/` project root:

```text
dark_eco/
├── README.md                                  # Main project documentation and architecture guide
├── chat_history.txt                           # Persistent record of research dialogue and instructions
├── dataset_inventory.csv                      # Comprehensive inventory of 26 remote sensing & ecological datasets
├── regional_availability_matrix.csv           # Regional availability, quality, and feasibility assessment matrix
│
├── data/
│   ├── raw/                                   # Immutable raw data archives (nightlights, GBIF, eBird, climate, DEM)
│   ├── processed/                             # Harmonized, cleaned, and gridded 5 km x 5 km raster & tabular arrays
│   └── metadata/                              # STAC metadata, variable definitions, and coordinate reference logs
│
├── geographical_boundaries/                   # GIS-compatible boundary and spatial framework layers
│   ├── study_areas_summary.geojson            # Multi-region bounding polygons in WGS84
│   ├── bengaluru_study_area.geojson           # 50 km x 50 km boundary for Bengaluru landscape
│   ├── mysuru_study_area.geojson              # 50 km x 50 km boundary for Mysuru landscape
│   ├── nilgiri_bandipur_study_area.geojson    # 50 km x 50 km boundary for Bandipur-Mudumalai landscape
│   ├── bengaluru_5km_grid.geojson             # 100 regular 5 km x 5 km cells (EPSG:32643 / WGS84)
│   ├── mysuru_5km_grid.geojson                # 100 regular 5 km x 5 km cells (EPSG:32643 / WGS84)
│   ├── nilgiri_bandipur_5km_grid.geojson      # 100 regular 5 km x 5 km cells (EPSG:32643 / WGS84)
│   └── all_regions_5km_grid.geojson           # Consolidated 300-cell spatial framework
│
├── scripts/
│   ├── phase_1_setup/                         # Boundary generation, grid construction, and inventory tooling
│   │   ├── generate_boundaries_and_grids.py   # Mathematical geodetic grid generator (UTM 43N -> WGS84)
│   │   └── generate_inventory_and_matrix.py   # Dataset metadata and regional availability compiler
│   ├── phase_2_nightlights/                   # Ingestion & harmonization (DMSP-OLS, VIIRS-DNB, Black Marble)
│   ├── phase_3_biodiversity/                  # Occurrence filtering, bias correction (GBIF, eBird, iNaturalist)
│   ├── phase_4_foodweb_traits/                # Interaction graphs & trait enrichment (GloBI, EltonTraits, AVONET)
│   └── phase_5_environment/                  # Land cover, canopy change, DEM, and climate reanalysis pipelines
│
└── reports/
    ├── geographical_framework.md              # In-depth spatial framework & bounding justification report
    ├── temporal_coverage_report.md            # Longitudinal coverage, sensor shifts, and trade-offs report
    ├── dataset_inventory/
    │   ├── dataset_inventory.csv              # Mirrored dataset source inventory
    │   └── regional_availability_matrix.csv   # Mirrored regional availability matrix
    ├── data_quality/                          # QA/QC audits, validation metrics, and sensor discontinuity checks
    └── phase_reports/
        └── phase_1_completion_report.md       # Comprehensive Phase 1 completion milestone report
```

---

## 3. Core Technical Principles & Precautions

1. **Strict Local Execution**: No code, data, or configuration is pushed to GitHub or remote repositories (`git push` is prohibited).
2. **Reproducibility**: All boundaries, grids, data cleaning routines, and graphs are constructed via deterministically versioned Python scripts.
3. **Data Integrity & Separation**: Raw data remains immutable in `data/raw/`; intermediate transformations and feature engineering reside strictly in `data/processed/`.
4. **Spatial Standardization**: All spatial computations use UTM Zone 43N (`EPSG:32643`) to guarantee exact metric distances (5,000 m × 5,000 m) with coordinates exported in standard `EPSG:4326` (WGS84).
5. **Sensor Harmonization**: Strict separation between raw radiometer signals (DMSP-OLS vs. VIIRS-DNB) and calibrated cross-sensor harmonized products (Chen et al. / Li et al.) to prevent artificial temporal artifacts in ML training.
