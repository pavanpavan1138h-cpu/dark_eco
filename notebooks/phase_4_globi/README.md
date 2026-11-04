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
   - Evaluates spatial reliability and traces source observation IDs to upstream iNaturalist metadata (confirming 100% traceability to 3,588 unique observations; live API verification of accuracy and geoprivacy flags).
   - Preserves all 4,522 canonical interaction events; inspects the 191 matching instances (10 exact duplicates vs 181 distinct repeated observations); generates the derived aggregated graph edge table (`globi_derived_aggregated_edges.csv`, $N = 4,120$ unique edges).
   - Reconciles CarniDIET 1.0 (684 rows down to 64 landscape-level predator-prey relationships across the 3 apex carnivores); cleanly separates 480 museum specimen vouchers from 4 literature records.
   - Replaces overloaded categories with an orthogonal 2D matrix: **Evidence Role (E1, E2, E3)** and **Spatial Reliability (S1, S2, S3, S4)**.
   - Master hierarchical count reconciliation across raw records, reciprocal pairs, canonical events, aggregated edges, and cell-level vs regional analysis suitability.

All notebooks are executed in-place with 0 errors and preserve all numerical and graphical outputs.

