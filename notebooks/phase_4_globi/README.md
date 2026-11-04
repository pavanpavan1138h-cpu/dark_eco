# Phase 4 Notebooks: GloBI Ecological Interaction Networks (`notebooks/phase_4_globi/`)

This directory contains the executed Jupyter Notebooks for **Phase 4: Global Biotic Interactions (GloBI) Investigation, Quality Audit, and Feasibility Analysis**.

## Notebook Directory Structure

1. **[`01_globi_api_and_source_investigation.ipynb`](01_globi_api_and_source_investigation.ipynb)**:
   - Evaluates the official GloBI REST API architecture (`https://api.globalbioticinteractions.org`).
   - Catalogs the 75 documented metadata terms from `/interactionFields`.
   - Proves that `includeObservations=true` is strictly required to extract empirical observation instances with geospatial coordinates and timestamps.
   - Tests pagination limits (`limit`, `offset`) and format handlers (`json`, `csv`, `tsv`).

2. **[`02_globi_regional_data_availability.ipynb`](02_globi_regional_data_availability.ipynb)**:
   - Executes spatial bounding box queries across Bengaluru (7,226 rows), Mysuru (946 rows), and Nilgiri–Bandipur (876 rows).
   - Audits coordinate completeness (100.0% populated) and study polygon containment (9,044 of 9,048 records inside study boundaries).
   - Spatially assigns records to the 100 5 km × 5 km grid cells per region (Bengaluru: 86/100, Mysuru: 49/100, Nilgiri–Bandipur: 28/100).
   - Analyzes temporal alignment with the approved 2012–2024 VIIRS/GBIF baseline.
   - Analyzes bidirectional symmetry (`eats` vs `eatenBy`, `preysOn` vs `preyedUponBy`).

3. **[`03_globi_sample_record_and_schema_audit.ipynb`](03_globi_sample_record_and_schema_audit.ipynb)**:
   - Granular record inspection across urban, peri-urban, and forest landscapes.
   - Traces contributing data provenance: iNaturalist citizen science (dominant in Bengaluru/Mysuru), CarniDIET carnivore scat survey (dominant in Nilgiri–Bandipur), and museum vouchers (UMMZ, MycoPortal, Ecdysis).
   - Field-by-field completeness matrix across 64 tabular columns.
   - Evaluates empirical observation records versus literature assertions.
   - Documents scientific biases (vagueness of `interactsWith`, urban park clustering, insect/mammal bias).

4. **[`04_globi_gbif_taxonomic_overlap.ipynb`](04_globi_gbif_taxonomic_overlap.ipynb)**:
   - Cross-references 1,206 unique GloBI taxa with 3,964 unique GBIF species (from 3.9M occurrences).
   - Identifies 615 direct binomial matches (51.0% exact species overlap).
   - Formulates ecological graph architecture for Temporal Graph Neural Networks (TGNNs) and multi-relational networks.
   - Evaluates graph connectivity, node-edge formulations, and constraints.

5. **[`05_globi_final_scientific_validation.ipynb`](05_globi_final_scientific_validation.ipynb)**:
   - **Task 1 — True CarniDIET Event Count**: Confirms `CarniDIET-Database` is a 100% clone duplicate of `GEB-2021-CarniDIET_database`. Removing 342 clone records leaves 342 unique directional assertions, forming exactly **171 canonical biological events** (73 Bandipur, 98 Mudumalai), not 342. Repeated measurements collapse into **86 site-specific predator–prey edges**.
   - **Task 2 — Reduction Reconciliation**: Explains why previous reports cited 183 and 256 reductions. Proves that the true reduction from canonical events to site edges is $171 - 86 = \mathbf{85}$ collapsed repeated measurement rows.
   - **Task 3 — Canonical Static Interaction Edges Reconciliation**: Traces progression from **2,562** (unnormalized) $\to$ **2,206** (active normalized) $\to$ **2,110** (`canonical_static_interaction_edges`, composed of 1,646 asymmetric directed + 464 symmetric canonical edges across 2,008 unique taxon pairs). Exported to [`globi_static_edges_mapping.csv`](../../data/metadata/phase_4_checks/globi_static_edges_mapping.csv).
   - **Task 4 — Master Event-Count Hierarchy & Orthogonal Partitions**:
     - Programmatically distinguishes raw API records (9,048), records inside polygons (9,044), peripheral records (4), unique inside assertions (8,702), unique canonical events (4,351), CarniDIET duplicate clone events (171), peripheral events (2), raw reciprocal pairs (4,524), and unique canonical events across the returned dataset (4,353).
     - Separates temporal classification (5,154 contemporary vs 3,548 historical) and spatial suitability (3,648 defensible, 632 ambiguous, 806 provisional, 3,616 regional-only) into orthogonal dimensions, proving that the 68 obscured records form their exact intersection.
   - **Task 5 — 2D Geospatial Grid-Cell Assignment & Provisional Records**: Metric buffer intersection in EPSG:32643 against the 5 × 5 km grid: `cell_defensible` (3,648 records / 1,824 events), `cell_boundary_ambiguous` (632 records / 316 events), `cell_provisional` (806 records / 403 events), `regional_only_obscured` (68 records / 34 events). For all 806 provisional records, original observation coordinates and point-in-polygon cell IDs are preserved (never replaced with cell centroids).
   - **Task 6 — Metric Comparison Table & Pass/Fail Checks**: 12 automated test assertions including three distinct event checks (inside before clone dedup: $4,351 + 171 = 4,522$; unique-event: $4,351 + 2 = 4,353$; raw-event: $4,522 + 2 = 4,524$), canonical static interaction edges integrity, and provisional spatial integrity, all executed with 100% pass rates and zero errors.

All notebooks are executed in-place with 0 errors and preserve all numerical and tabular outputs.
