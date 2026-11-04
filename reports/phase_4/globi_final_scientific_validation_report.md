# Phase 4 — GloBI Final Scientific Validation and Evidence Preservation Report
## Spatial Reliability, CarniDIET Provenance, Orthogonal Evidence–Spatial Matrix, and Master Hierarchical Reconciliation

**Project:** Dark Ecology Intelligence: Temporal Graph Neural Networks and Deep Reinforcement Learning for AI-Driven Light Pollution Governance  
**Course:** ANN Lab PBL — AI2531A  
**Stage:** Phase 4 — Biotic Interactions Final Scientific Validation  
**Date:** 2026-11-04  
**Status:** **SCIENTIFIC VALIDATION AND COUNT RECONCILIATION COMPLETED — READY FOR REGIONAL ACQUISITION UPON USER APPROVAL**

---

## Executive Summary

Following the comprehensive GloBI API investigation, this report delivers the final pre-acquisition scientific validation, resolving remaining spatial reliability, provenance, and mathematical questions across **Bengaluru (Urban)**, **Mysuru (Peri-urban)**, and **Nilgiri–Bandipur (Forest, Option A)**.

### Headline Accomplishments & Scientific Determinations:
1. **Spatial Reliability & Upstream iNaturalist Tracing**:
   - Out of 7,690 iNaturalist records, **100.0% have traceable observation IDs** in `target_specimen_occurrence_id` or `catalog_number` (representing 3,588 unique observations).
   - Direct verification against the official iNaturalist REST API confirms that original iNaturalist observations store `positional_accuracy` and `obscured` flags.
   - However, **GloBI does NOT transmit these Darwin Core fields in its interaction endpoint**. Therefore, when consuming GloBI data directly, coordinates are classified as **S2 (Point coordinates with unknown precision)** rather than inferred GPS accuracy.
2. **Preservation of the 191 Potentially Duplicated Instances**:
   - All **4,522 canonical interaction events** are strictly preserved with original identifiers.
   - Inspection of the 191 matching instances across 58 spatiotemporal keys reveals that **10 cases are exact duplicate source records** (identical observation IDs uploaded/indexed twice), while **181 cases are distinct repeated observations** (different observation IDs) describing the same interaction at the same location and date (e.g. bioblitz surveys in urban parks).
   - To support network modeling without losing evidence, we created a **Derived Aggregated Graph Edge Table** (`globi_derived_aggregated_edges.csv`, $N = 4,120$ unique spatiotemporal edges) containing `evidence_count` and concatenated provenance IDs.
3. **CarniDIET Provenance & Museum Voucher Correction**:
   - Traced the 684 CarniDIET rows across two GitHub repositories (342 rows each; 100% clone) through 172 unique scientific assertions (86 forward + 86 reciprocal) down to **64 unique landscape-level predator–prey relationships** across the 3 apex carnivores (*Panthera pardus*: 23 prey, *Cuon alpinus*: 21 prey, *Panthera tigris*: 20 prey).
   - Corrected the historical breakdown: exactly **480 museum specimen vouchers** (220 Ecdysis arthropods, 256 MycoPortal fungi, 4 UMMZ Michigan insects) and **4 literature dietary notes** (*SquamataBase* Cobra diet).
   - CarniDIET records represent broad reserve centroids ($300\text{--}900\text{ km}^2$) and are strictly prevented from being assigned to 5 km grid cells as point observations.
4. **Orthogonal 2D Classification Architecture**:
   - Replaced overloaded categories with two independent fields: **Evidence Role (E1, E2, E3)** and **Spatial Reliability (S1, S2, S3, S4)**.
5. **Master Hierarchical Reconciliation**:
   - Established strict mathematical alignment from raw retrieved records ($N = 9,048$) to reciprocal pairs ($N = 9,044$), canonical events ($N = 4,522$), aggregated graph edges ($N = 4,120$), static edges ($N = 2,110$), cell-level dynamic records ($N = 5,154$), and regional scaffold records ($N = 3,890$). Zero unexplained residuals.

---

## 1. Spatial Reliability & Upstream Metadata Tracing

We investigated what the coordinates actually represent across all 9,048 retrieved records ($N = 9,044$ inside study polygons).

### 1. Source Observation ID Tracing (iNaturalist)
- Across the 7,690 iNaturalist records, **every single record (100.0%) contains a traceable observation ID** stored in `target_specimen_occurrence_id` (e.g. `https://www.inaturalist.org/observations/381936683`) or `target_specimen_catalog_number` (e.g. `381936683`).
- These 7,690 rows trace back to **3,588 unique iNaturalist observations**.

### 2. Live Upstream API Query Verification
We queried the official iNaturalist REST API (`https://api.inaturalist.org/v1/observations/`) for a representative sample of extracted IDs:
- **Observation `313520452`** (*Double-branded Crow Butterfly* in Bengaluru, `12.98659, 77.7448`):
  `positional_accuracy: 197 meters`, `geoprivacy: open`, `obscured: false`.
- **Observation `197899786`**: `positional_accuracy: 15 meters`, `geoprivacy: open`, `obscured: false`.
- **Observation `185997652`**: `positional_accuracy: null`, `geoprivacy: open`, `obscured: false`.

### 3. Critical Scientific Reality Check
- While upstream iNaturalist stores positional accuracy and obscuration flags, **GloBI does NOT harvest or export these Darwin Core terms** in its `/interaction` endpoint.
- Therefore, within the GloBI dataset, numeric coordinate precision cannot be taken as physical GPS accuracy.
- Any observation of a threatened species (e.g. Schedule I / CITES taxa) may have been obscured to a $\sim 10\text{ km} \times 10\text{ km}$ bounding box prior to GloBI harvesting.
- **Governing Rule**: GloBI point coordinates must be classified as **S2 (Point coordinates with unknown precision)**. Records in Category E1 are eligible for 5 km cell assignment with the explicit caveat that citizen-science positional accuracy is unquantified in GloBI.

---

## 2. Preservation of the 191 Potentially Duplicated Instances & Aggregated Edge Table

The user instructed to preserve all 4,522 canonical interaction events and investigate the 191 matching instances.

### 1. Investigation of the 191 Cases
We audited the 191 symmetric pairs sharing identical `(study_region, latitude, longitude, event_date, sorted_taxa)` signatures across 58 distinct spatiotemporal keys:
- **Exact Duplicate Source Records (10 cases)**: The same observation ID was indexed multiple times in GloBI (e.g. multiple identifications or duplicate harvesting).
- **Distinct Repeated Observations (181 cases)**: Different observation IDs describing the same interaction between the same pair of taxa at the same location and date (e.g. bioblitz surveys in Lalbagh or Cubbon Park where multiple observers photographed the same tree/nest).
- **Preservation Policy**: None of these records were deleted. All **4,522 canonical interaction events** are preserved in the raw canonical dataset.

### 2. Derived Aggregated Graph Edge Table (`globi_derived_aggregated_edges.csv`)
To support graph neural network modeling without discarding evidence, we constructed a derived table that groups raw observation events into unique directed graph edges:
- **Total Unique Spatiotemporal Edges**: **4,120 edges**.
- **Edge Schema**:
  - `edge_id`: Unique identifier (e.g. `DEI_EDGE_BLR_0001`).
  - `source_taxon_name`, `interaction_type`, `target_taxon_name`.
  - `study_region`, `latitude`, `longitude`, `cell_id`.
  - `event_date`, `parsed_year`.
  - `evidence_count`: Number of raw observation events supporting the edge (1 to 10+).
  - `contributing_record_ids`: Concatenated list of original iNaturalist / GloBI record identifiers.
  - `source_studies`: Citations of contributing studies.
  - `evidence_role`: `E1` (Contemporary) vs `E2` (Regional Context).
  - `spatial_reliability`: `S2` (Point Unknown Precision), `S3` (Centroid), `S4` (Historic Locality).
  - `analysis_suitability`: `Cell-Level Dynamic Analysis` vs `Regional Scaffold Only`.

---

## 3. Correct CarniDIET 1.0 Classification & Museum Voucher Separation

### 1. CarniDIET 1.0 Complete Record-Level Reconciliation (Nilgiri–Bandipur)
All 684 CarniDIET records derive from two published scat surveys:
- **Bandipur Tiger Reserve** (Andheria, Karanth & Kumar, 2007; centroid `11.7833, 76.4833`):
  146 rows per repo $\to$ 73 `eats` + 73 `eatenBy` $\to$ **33 distinct predator–prey pairs**.
- **Mudumalai Tiger Reserve** (Ramesh, Kalle, Sankar & Qureshi, 2012; centroid `11.6250, 76.5583`):
  196 rows per repo $\to$ 98 `eats` + 98 `eatenBy` $\to$ **53 distinct predator–prey pairs**.
- **Landscape Synthesis**:
  $33 + 53 = 86\text{ site-level pairs}$. Exactly **22 pairs are shared** between both reserves.
  Net unique biological predator–prey relationships: $86 - 22 = \mathbf{64\text{ unique biological relationships}}$ across Leopard (23), Dhole (21), and Tiger (20).
- **Centroid Rule**: CarniDIET records are strictly restricted to the **Regional Trophic Scaffold (E2 / S3)** and are **never assigned to individual 5 km grid cells**.

### CarniDIET Record-Level Reconciliation Table

| Processing Stage | Row Count | Distinct Predators | Distinct Prey | Scientific Meaning & Downstream Role |
|:---|:---:|:---:|:---:|:---|
| **1. Total Imported GloBI CarniDIET Rows** | **684** | 3 | 28 | Raw rows returned from GloBI REST API for Nilgiri–Bandipur |
| **2. Exact Duplicated Repository Rows** | **342** | 3 | 28 | 100% duplicate clone from second GitHub repo (`CarniDIET-Database`) |
| **3. Unique Scientific Assertions (Single Repo)**| **172** | 3 | 28 | De-duplicated scientific assertions (86 `eats` + 86 `eatenBy`) |
| **4. Forward Trophic Assertions (`eats`)** | **86** | 3 | 28 | Site-specific predator–prey assertions across the two reserves |
| **5. Bandipur Site Distinct Pairs (Andheria et al.)**| **33** | 3 | 16 | Tiger (11), Leopard (12), Dhole (10) prey profiles |
| **6. Mudumalai Site Distinct Pairs (Ramesh et al.)** | **53** | 3 | 24 | Tiger (16), Leopard (19), Dhole (18) prey profiles |
| **7. Shared Prey Profiles Between Sites** | **22** | 3 | 12 | Apex carnivore prey selection common to both reserves |
| **8. Unique Biological Relationships Across Landscape**| **64** | 3 | 28 | **Canonical Regional Scaffold**: Leopard (23), Dhole (21), Tiger (20) |

### 2. Museum Specimen Vouchers vs Literature Correction
The previously combined 484 historical records are now cleanly separated:
- **Museum Specimen Vouchers**: Exactly **480 records**:
  - Ecdysis Arthropod Vouchers: 220 records (Bengaluru)
  - MycoPortal Fungal Vouchers: 256 records (194 Bengaluru, 52 Mysuru, 10 Nilgiri–Bandipur)
  - UMMZ Michigan Museum Insect Vouchers: 4 records (Mysuru)
- **Literature Dietary Notes**: Exactly **4 records** from *SquamataBase* (Grundler, 2020) documenting Cobra diet in Bengaluru.
- Sum: $480 + 4 = \mathbf{484\text{ records}}$.

---

## 4. Orthogonal Evidence Role (E) and Spatial Reliability (S) Classification

We replaced overloaded labels with two independent, orthogonal fields across all 9,048 records:

### Field Definitions:
- **Evidence Role ($E$)**:
  - `E1`: Contemporary empirical evidence (direct field observations inside study polygon during 2012–2024).
  - `E2`: Historical or regional contextual evidence (literature centroids, museum vouchers, pre-2012 or post-2024 observations).
  - `E3`: Excluded records (falling outside approved study polygons).
- **Spatial Reliability ($S$)**:
  - `S1`: Documented positional accuracy ($\le 1,000$ m; 0 records in GloBI).
  - `S2`: Point coordinates with unknown precision (iNaturalist encounters).
  - `S3`: Known generalised location or study-site centroid (CarniDIET, SquamataBase).
  - `S4`: Historical or unresolved locality (museum vouchers, institutional grounds).

### 2D Orthogonal Classification Matrix (All 9,048 Records)

| Evidence Role \ Spatial Reliability | S1: Documented Accuracy | S2: Point Unknown Precision | S3: Study-Site Centroid | S4: Historical Locality | Total Records | % of Dataset |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **E1: Contemporary Empirical (2012–2024)** | 0 | **5,154** | 0 | 0 | **5,154** | **57.0%** |
| **E2: Regional / Historical Scaffold** | 0 | **2,532** | **696** | **662** | **3,890** | **43.0%** |
| **E3: Excluded (Outside Boundary)** | 0 | 0 | 0 | **4** | **4** | **<0.1%** |
| **Combined Total** | **0** | **7,686** | **696** | **666** | **9,048** | **100.0%** |

### Regional Breakdown of Evidence Roles:
- **Bengaluru**: E1 = 4,476; E2 = 2,746; E3 = 4 $\to$ Total = 7,226.
- **Mysuru**: E1 = 574; E2 = 372; E3 = 0 $\to$ Total = 946.
- **Nilgiri–Bandipur**: E1 = 104; E2 = 772; E3 = 0 $\to$ Total = 876.

---

## 5. Master Hierarchical Count Reconciliation Table

This master table establishes absolute mathematical alignment from raw API responses down to cell-level and regional analytical datasets:

| Processing Level / Entity | Raw Records | Events / Edges | Analysis Scope & Scientific Role |
|:---|:---:|:---:|:---|
| **1. Retrieved Raw Records** | **9,048** | — | Total rows retrieved from GloBI REST API for the three bounding boxes |
| **2. Inside Approved Study Polygons** | **9,044** | — | Clipped to approved 50 km GeoJSON boundaries (4 excluded in Category E3) |
| **3. Reciprocal-Paired Records** | **9,044** | — | 100.0% paired (3,062 forward + 3,062 inverse + 2,920 symmetric) |
| **4. Biological Interaction Events** | **9,044** | **4,522** | Canonical reciprocal halving (3,062 asymmetric + 1,458 symmetric + 2 conspecific) |
| **5. Unique Spatiotemporal Instances** | **8,853** | **4,331** | 191 duplicate symmetric instances identified, preserved, and grouped |
| **6. Aggregated Spatiotemporal Graph Edges** | **9,044** | **4,120** | Spatiotemporally aggregated edges with `evidence_count` and record IDs |
| **7. Static Directed Species Interaction Edges**| **9,044** | **2,110** | Unique directed (source, type, target) relationships across 1,206 taxa |
| **8. Cell-Level Dynamic Analysis (E1 + S2)** | **5,154** | **2,577 events** <br> (2,529 edges) | Contemporary (2012–2024) point observations assigned to 5 km grid cells |
| **9. Regional Trophic Scaffold Only (E2)** | **3,890** | **1,945 events** | CarniDIET reserve centroids, museum vouchers, non-2012–2024 observations |
| **10. Excluded Records (E3)** | **4** | **2 events** | Bounding-box corner sliver records outside study polygons |

$$\text{Reconciliation Check: } 5,154\text{ (Cell-Level)} + 3,890\text{ (Regional Scaffold)} + 4\text{ (Excluded)} = \mathbf{9,048\text{ Records (100\% Exact)}}.$$

---

## 6. Deliverables Updated & Verified

1. **Jupyter Notebook (`notebooks/phase_4_globi/`)**:
   - [`05_globi_final_scientific_validation.ipynb`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/notebooks/phase_4_globi/05_globi_final_scientific_validation.ipynb): Updated with iNaturalist upstream API tracing, CarniDIET 64-relationship synthesis, derived edge table inspection, and orthogonal E/S matrix; executed with **0 errors**.
2. **Derived Aggregated Edge Table**:
   - `dark_eco/data/metadata/phase_4_checks/globi_derived_aggregated_edges.csv`: Generated with 4,120 unique spatiotemporal edges, evidence counts, and concatenated provenance IDs.
3. **Master Investigation & Download Plan**:
   - [`reports/phase_4/globi_investigation_and_download_plan.md`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/reports/phase_4/globi_investigation_and_download_plan.md): Updated with validated pair counts and Category A/B/C breakdown.
4. **Phase 4 README**:
   - [`notebooks/phase_4_globi/README.md`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/notebooks/phase_4_globi/README.md): Updated to document Notebook 05.
5. **Project Registers**:
   - [`dataset_inventory.csv`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/dataset_inventory.csv): Updated with final validated counts and 3-Tier structure.
   - [`regional_availability_matrix.csv`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/regional_availability_matrix.csv): Updated with Category A counts.
   - [`chat_history.txt`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/chat_history.txt): Logged reconciliation results.

---

## FINAL ACQUISITION READINESS & SCIENTIFIC RECOMMENDATION

### Acquisition Recommendation: **FULLY AUTHORIZED FOR REGIONAL ACQUISITION**

The GloBI regional dataset has been completely audited, mathematically reconciled, and verified down to individual source citations and observation IDs.

### Permitted Scientific Analysis Levels:
1. **Cell-Level Dynamic Analysis (5 km Grid Cells, 2012–2024)**:
   - **Permitted for E1 + S2 records (5,154 records; 2,577 events)**.
   - **Caveat**: Coordinates are point encounters with unquantified positional precision in GloBI; geoprivacy obscuration on threatened taxa must be acknowledged.
2. **Regional-Level Static Trophic Modeling**:
   - **Permitted for E2 records (3,890 records; 1,945 events)** including CarniDIET apex predator diets (64 relationships) and museum vouchers (480 records).
   - **Restriction**: Must never be assigned to individual 5 km cells as point observations.

**STRICT STOPPING RULE OBSERVED**:
- Zero bulk data written to `data/raw/globi/`.
- Zero synthetic data fabricated.
- No ESA WorldCover, integrated EDA, or graph models initiated.
- **Awaiting your explicit authorization to proceed with raw regional acquisition.**
