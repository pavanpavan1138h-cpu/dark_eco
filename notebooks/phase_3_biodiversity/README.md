# Phase 3 Notebooks: GBIF Biodiversity Occurrences (`notebooks/phase_3_biodiversity/`)

This directory contains the executed Jupyter Notebooks for **Phase 3: GBIF Biodiversity Occurrence Data Collection, Investigation and Validation**.

## Executed Notebooks Inventory

1. **`01_gbif_source_investigation.ipynb`**:
   - Technical investigation of official GBIF REST endpoints (`/occurrence/search`, `/occurrence/count`, `/occurrence/download/request`).
   - Evaluation of search API pagination constraints (`limit=300`, `offset=100,000` ceiling).
   - Darwin Core Standard (DwC) terms and licensing schema (CC0, CC BY, CC BY-NC).
   - Exploration vs registered citable DOI download architecture.

2. **`02_gbif_api_and_query_validation.ipynb`**:
   - Geometrical query reproduction across the three 50 km × 50 km study windows.
   - Exact mathematical comparison between axis-aligned Bounding Box (BBOX) and exact UTM Zone 43N conformal Polygon (WKT).
   - Discrepancy explanation: elimination of peripheral out-of-bounds records (Bengaluru: -6,668, Mysuru: -642, Nilgiri–Bandipur: -768).

3. **`03_gbif_temporal_coverage.ipynb`**:
   - Multi-decadal temporal distribution from historical museum collections (1800–1837) to 2024.
   - Analysis of the post-2014 citizen science explosion (eBird India surge).
   - Validation that the aligned 2012–2024 decadal window captures **80% to 83% of all historical records** (>3.9 million records).
   - Intra-annual seasonality and documentation of Southwest Monsoon observer slump (June–August).

4. **`04_gbif_taxonomic_and_dataset_bias.ipynb`**:
   - Taxonomic distribution across kingdoms, phyla, and classes.
   - Quantification of extreme Class Aves (bird) dominance (>96.7% across all regions).
   - Non-avian taxa accounting: Insecta (~1.0–1.4%), Magnoliopsida (~0.4–0.8%), Mammalia (~0.04–1.01%), Squamata, Amphibia.
   - Data publisher breakdown: eBird Observation Dataset (Cornell Lab of Ornithology) contributing >94.8%–97.0%, iNaturalist Research-Grade contributing 2.5%–2.8%.

5. **`05_gbif_coordinate_and_record_quality.ipynb`**:
   - Coordinate precision and `coordinateUncertaintyInMeters` investigation.
   - The ~97% missing coordinate uncertainty phenomenon explained (eBird submission protocol default).
   - Justification against naive uncertainty filtering to prevent discarding >96% of valid bird data.
   - Geospatial quality flags audit (`hasGeospatialIssue=false` for >99.99% of records).

6. **`06_gbif_spatial_grid_analysis.ipynb`**:
   - Spatial census across all 300 5 km × 5 km conformal grid cells (100 cells per region).
   - Verification of 100% cell occupancy (0 empty cells; minimum 2 records, median 413 to 10,414).
   - Extreme spatial inequality quantification: Lorenz curves and exact Gini coefficients (0.7183 in Bengaluru, 0.7905 in Mysuru, 0.8167 in Nilgiri–Bandipur).
   - Road and urban park accessibility bias (Lalbagh, Cubbon Park, Karanji Lake, Masinagudi strip).

7. **`07_gbif_indicator_feasibility.ipynb`**:
   - Rigorous scientific feasibility assessment for candidate biodiversity indicators.
   - Complete record count reconciliation across all 3 landscapes and 300 grid cells (3,901,020 clean records).
   - Geodesic and mathematical proof of the 561 unassigned Bengaluru records as meridian convergence slivers ($0.0\text{ m}^2$ symmetric difference in UTM 43N), handled via `outside_grid_assignment`.
   - Reassessment of Bandipur zero-observation cell `NB_R10_C04` (human observer effort deficiency $\neq$ ecological absence; reserve core restrictions framed as a hypothesis).
   - In-depth schema audit of `SIMPLE_CSV` vs `DWCA`: verification that `DWCA` preserves `eventID` (100% of eBird records), enabling checklist clustering for birds, while `SIMPLE_CSV` strips `eventID`.
   - Downgrade of Sample-Based Rarefaction to **EXPLORATORY / CONDITIONAL (BIRDS ONLY)** due to missing duration/distance metrics and non-avian data absence.
   - Reclassification of Occupancy Modeling ($\psi$) as NOT SUPPORTED (presence-only records; zero synthetic data rule).
   - Recommendation of `DWCA` format for registered bulk download.
   - Validated GBIF Download Predicate: `or` container with 3 closed, CCW WKT study polygons generating a permanent citable DOI (~3.9M clean records).

8. **`08_gbif_dwca_archive_verification.ipynb`**:
   - Comprehensive empirical verification of the downloaded Darwin Core Archive (`0025038-261023074918325`, DOI `10.15468/dl.rum47g`).
   - Archive descriptor (`meta.xml`) and 230-column occurrence schema inspection.
   - Exact record count validation: 3,901,020 records (Bengaluru: 2,947,292, Mysuru: 761,890, Nilgiri–Bandipur: 191,838; Delta = 0).
   - Bengaluru spatial grid assignment verification: 2,946,708 records inside 100 cells, 584 records in southern meridian sliver flagged as `outside_grid_assignment` (cell_id = None).
   - `eventID` completeness and checklist clustering analysis: 97.6% overall; 99.2% for Class Aves; missingness audit across taxonomic classes.
   - Missingness audit: `samplingProtocol` (99.94% null), `coordinateUncertaintyInMeters` (97.84% null), absence of true non-detections.
   - Final certification of data integrity and presence-only modeling governance.

9. **`09_gbif_final_reconciliation.ipynb`**:
   - Focused independent reconciliation of the four critical review issues.
   - Geodetic resolution of the 23-record Bengaluru grid discrepancy: proved that northern meridian curvature of Row 10 cells (`BLR_R10_C04` [+4] and `BLR_R10_C07` [+19]) extended beyond the 4-vertex straight outer chord used in the bulk download predicate.
   - Verified final Bengaluru grid partition: 2,946,708 inside 100 cells; 584 in southern sliver (`outside_grid_assignment`, cell_id = None); total = 2,947,292 clean records.
   - Taxonomic and source-specific `eventID` completeness audit: eBird birds (100.0% with `eventID`), non-eBird birds (0.13% with `eventID`), non-avian taxa (14.64% with `eventID` overall; 98.4% missing for fauna; 44.9% with `eventID` in plants via SeasonWatch/IISc).
   - `individualCount` semantic audit: established as reported encounter counts of detected individuals during visits (NULL = "X"), explicitly distinguished from observer count, survey effort, and population abundance/density.
   - Official GBIF provenance verification: verified against `api.gbif.org/v1/occurrence/download/0025038-261023074918325`, explaining Apache Oozie cluster timestamp syntax (`261023074918325`) vs actual submission time (`2026-11-03T15:49:20.852Z`).

*Note: All 9 Phase 3 notebooks are fully executed in-place with outputs preserved.*
