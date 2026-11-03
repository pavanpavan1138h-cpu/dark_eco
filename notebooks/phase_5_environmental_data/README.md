# Phase 5 Notebooks: Environmental Data (`notebooks/phase_5_environmental_data/`)

This directory will contain the notebooks for **Phase 5: Land Cover, Forest Dynamics, Topography, and Climate Covariates**.

## Planned Workflows (Phase 5)

- **`01_environmental_source_investigation.ipynb`**: Evaluation of spatial resolutions, projection systems, and temporal epochs across environmental layers.
- **`02_data_collection.ipynb`**: Direct downloading and spatial subsetting of ESA WorldCover (10m), Hansen Global Forest Change (30m), Copernicus DEM (30m), WorldPop (100m), GHSL (100m), and ERA5-Land (~9km).
- **`03_data_inspection_quality.ipynb`**: QA/QC auditing of raster alignments, topographic slope/aspect calculations, and water body masks.
- **`04_data_preprocessing.ipynb`**: Zonal statistics aggregation of land cover fractions, annual forest loss, population density, elevation, and climate time series to each 5 km × 5 km cell.
- **`05_dataset_consolidation_validation.ipynb`**: Synthesis into a unified multi-modal spatio-temporal dataset with cross-validation checks against BioTIME, PREDICTS, and NTCA reports.

*Note: Phase 5 will begin only after Phase 4 approval.*

