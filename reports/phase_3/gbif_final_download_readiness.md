# Dark Ecology Intelligence (DEI) — Phase 3: Biodiversity Occurrences
# FINAL GBIF DOWNLOAD READINESS AUDIT REPORT

**Project**: Dark Ecology Intelligence (DEI) — Artificial Neural Networks Problem-Based Learning (ANN PBL)  
**Audit Date**: November 2026  
**Auditor Role**: Scientific Research Data Engineer & Ecological Quality Auditor  
**Scope**: Final Download Readiness Audit, Bengaluru Grid Geodesic Analysis, Bandipur Cell Review, DWCA Archive Specification, and Rarefaction Feasibility Assessment  
**Governing Rule**: Strict Evidence-Based Assessment | Zero Synthetic Data | No Bulk Download Executed | No Remote Git Push  

---

## Final Readiness Verdict

# **VERDICT: READY FOR APPROVAL**

The proposed registered download query, spatial geometry predicates, temporal filters, and quality parameters have been rigorously audited against official GBIF API architecture and empirical repository counts. No technical, spatial, or mathematical discrepancies remain unresolved. The download is certified ready for submission upon formal user authorization.

---

## 1. Bengaluru Grid Geometry, Geodesic Analysis & the 561 Unassigned Records

### Audited Discrepancy Analysis
A systematic reconciliation was conducted between:
- The single outer study area polygon queries (`study_areas_summary.geojson`).
- The sum of the 100 conformal 5 km × 5 km grid cells (`all_regions_5km_grid.geojson`).
- The all-historical records versus the 2012–2024 target decadal window.

```
Comprehensive Regional Record Count Reconciliation Matrix:
==============================================================================================================================================
Landscape             All-History    2012–2024      2012–2024      100 Cells Sum   100 Cells Sum   Unassigned Records  Grid Handling
                      Outer Polygon  Outer Polygon  Clean (Target) (All-History)   (2012–2024)     (Curvilinear Sliver)
----------------------------------------------------------------------------------------------------------------------------------------------
Bengaluru (Urban)       3,558,771      2,947,294      2,947,292      3,558,133       2,946,731             561         Flagged outside_grid
Mysuru (Peri-Urban)       937,184        761,891        761,890        937,184         761,890               0         All assigned
Nilgiri-Bandipur          240,252        191,838        191,838        240,251         191,838               0         All assigned
----------------------------------------------------------------------------------------------------------------------------------------------
COMBINED ARCHIVE        4,736,207      3,901,023      3,901,020      4,735,568       3,900,459             561         Preserved regionally
==============================================================================================================================================
```

### Categorical Breakdown per Study Window (2012–2024 Clean Target):
1. **Bengaluru**: 
   - Outer polygon query: **2,947,292 clean records** (2 geospatial issues excluded).
   - Sum of 100 cells: **2,946,731 records**.
   - Unassigned records: **561 records**.
2. **Mysuru**: 
   - Outer polygon query: **761,890 clean records** (1 geospatial issue excluded).
   - Sum of 100 cells: **761,890 records**.
   - Unassigned records: **0 records** (100.0% assignment).
3. **Nilgiri–Bandipur**: 
   - Outer polygon query: **191,838 clean records** (0 geospatial issues excluded).
   - Sum of 100 cells: **191,838 records**.
   - Unassigned records: **0 records** (100.0% assignment).
4. **Total Archive**: **3,901,020 clean records**. Sum across 300 cells: **3,900,459 records**. Exactly **561 unassigned records** located exclusively along the southern Bengaluru boundary.

---

### Geometric and Mathematical Cause of the 561-Record Discrepancy

A rigorous GIS audit was conducted to verify the coordinate reference systems, transformations, and geometric areas of the Bengaluru outer boundary versus its 100 grid cells:

| Geometric Metric | Outer Study Area Boundary (`bengaluru_study_area.geojson`) | Union of 100 Grid Cells (`bengaluru_5km_grid.geojson`) | Symmetric Difference |
| :--- | :---: | :---: | :---: |
| **Geographic CRS (WGS 84, EPSG:4326)** | $0.20803651\text{ deg}^2$ | $0.20803651\text{ deg}^2$ | **$7.5123 \times 10^{-5}\text{ deg}^2$** |
| • *Outer minus Grid Union Area* | — | — | **$3.7560 \times 10^{-5}\text{ deg}^2$** (~0.45 km²) |
| • *Grid Union minus Outer Area* | — | — | **$3.7563 \times 10^{-5}\text{ deg}^2$** (~0.45 km²) |
| **Projected Metric CRS (UTM 43N, EPSG:32643)**| $2,500,000,000.0\text{ m}^2$ ($2,500.00\text{ km}^2$) | $2,500,000,000.0\text{ m}^2$ ($2,500.00\text{ km}^2$) | **$0.0\text{ m}^2$ (Exact identity)** |

#### Geodesic Mechanics — Meridian Convergence:
1. **Design Space**: The 50 km × 50 km study windows and 5 km × 5 km grid cells were designed in projected metric space (UTM Zone 43N, EPSG:32643). In UTM 43N, the outer polygon and the union of the 100 cells have an identical area of $2,500.00\text{ km}^2$ and a symmetric difference of **exactly $0.0\text{ m}^2$**.
2. **Transformation to Geographic Storage (WGS 84)**: When coordinates are transformed to WGS 84 degrees (EPSG:4326), lines of constant grid Northing ($Y = 1,410,000\text{ m}$) are curved due to meridian convergence (central meridian $75^\circ\text{ E}$; Bengaluru centroid $\sim 77.59^\circ\text{ E}$).
3. **Vertex Density Difference**:
   - The outer study polygon in GeoJSON has only **4 vertices**, connecting the four 50-km corners via straight chords in $(\text{longitude}, \text{latitude})$ degree space.
   - The 100 grid cells have **40 perimeter segments** (ten 5-km chords per side), tracking the curved UTM constant-northing boundary with 10 times finer resolution.
   - Along the southern boundary, the straight 50-km chord bows southward by up to $\sim 45\text{ m}$ relative to the true UTM boundary, creating a tiny crescent sliver of $3.756 \times 10^{-5}\text{ deg}^2$.
4. **Empirical Verification of Records in the Sliver**:
   - Empirical query of this sliver geometry in GBIF confirmed exactly where these unassigned records fall.
   - Transforming sample points (e.g. Lat $12.741977^\circ\text{ N}$, Lon $77.578873^\circ\text{ E}$) to UTM Zone 43N yields:
     - $\text{Easting} = 780,028.52\text{ m}$
     - $\text{Northing} = 1,409,992.88\text{ m}$
   - The minimum Northing of the Bengaluru study grid is $Y_{\min} = 1,410,000.00\text{ m}$.
   - The record lies **$7.12\text{ m}$ south of the study window**!
   - Therefore, these 561 records are **genuinely outside the 100-cell grid union**.

---

### Data Handling Policy & Analytical Implications for the 561 Records

1. **Preservation in Regional Dataset**:
   All 561 records will be retained in the downloaded regional occurrence archive. They are legitimate empirical observations within the broader Bengaluru landscape. Total regional clean records = **2,947,292**.
2. **Explicit Flagging for Grid-Level Analysis**:
   These 561 records cannot be assigned reliably to any of the 100 grid cells without violating geometric containment. They will be flagged as:
   ```
   grid_assignment_status = "outside_grid_assignment"
   cell_id = None
   ```
3. **Strict Prohibition of Force-Assignment**:
   These records must **NOT** be artificially shifted, snapped, or force-assigned to row 1 grid cells (e.g. `BLR_R01_C05`). Force-assigning points that lie outside the cell boundary introduces artificial density spikes and spatial bias.
4. **Implications for Research**:
   - **Regional Landscape Analyses** (overall species lists, regional temporal trends): Uses all **2,947,292** records.
   - **Grid-Level Analyses** (5 km × 5 km cell metrics, VIIRS ALAN regressions): Uses exactly **2,946,731** records across the 100 cells. The 561 unassigned records represent only **0.019%** of the regional data and do not distort cell-level biodiversity metrics.

---

## 2. Bandipur Zero-Observation Cell NB_R10_C04

### Empirical Audit:
- **Cell Identifier**: `NB_R10_C04` (Row 10, Col 4 of Nilgiri-Bandipur 5 km grid).
- **Centroid Coordinates**: Lat $11.859735^\circ\text{ N}$, Lon $76.528547^\circ\text{ E}$.
- **UTM Coordinates**: Easting $[664000, 669000]\text{ m}$, Northing $[1309000, 1314000]\text{ m}$.
- **2012–2024 Clean Record Count**: **Exactly 0 records**.
- **All-History Record Count**: **2 records** (both recorded in early 2026).

---

### Scientific Interpretation & Removal of Unsupported Claims

1. **Hypothesis vs. Proven Cause**:
   - Previous preliminary notes suggested that restricted reserve access was the proven cause of zero observations. **This claim has been removed.**
   - While cell `NB_R10_C04` intersects the core protected zone of Bandipur Tiger Reserve where public pedestrian and unauthorized vehicular access is restricted under the Wildlife (Protection) Act, 1972, reserve access restrictions represent **only a plausible hypothesis**, not an established empirical proof.
   - In the absence of authoritative visitor GPS tracking logs or forest department trail access records, other contributing factors cannot be ruled out:
     - Absence of motorable tracks or public roads within this specific 25 km² parcel.
     - Birder and tourist preference for established safari circuits located elsewhere in the park.
     - Dense dry-deciduous / moist-deciduous canopy reducing bird detectability.
     - Lack of mobile cellular network connectivity preventing mobile app checklist uploads.
2. **Fundamental Ecological Axiom**:
   - **Zero GBIF observations do NOT establish ecological absence.**
   - In opportunistic citizen-science presence-only data, zero records reflect **zero recorded human observation effort**, not the absence of wildlife.
   - Protected core forests in the Western Ghats / Nilgiri Biosphere Reserve harbor rich native biodiversity, large mammal populations (elephants, tigers, gaurs), and diverse avifauna despite the complete absence of recreational birding checklists.
   - Machine learning models must treat `NB_R10_C04` as **unobserved / effort-censored**, never as an ecological void.

---

## 3. DWCA Archive Specification & eBird Record Architecture

We investigated the official GBIF Darwin Core Archive (`DWCA`) specification (`https://api.gbif.org/v1/occurrence/download/describe/dwca`) and probed empirical eBird and non-eBird records across the three study landscapes:

### Side-by-Side Schema Comparison:

| Technical Attribute | `SIMPLE_CSV` (Flat TSV) | `DWCA` (`occurrence.txt`) | Empirical Findings in DEI Study Landscapes |
| :--- | :---: | :---: | :--- |
| **`eventID` Included?** | **NO** (50 columns total) | **YES** (230 interpreted fields) | Retained in `DWCA`. Populated in **100%** of eBird records. |
| **eBird Checklist ID?** | **NO** (Omitted) | **YES** (e.g. `S159324143`) | Preserves the exact eBird submission checklist ID. |
| **Taxonomic Scope of `eventID`**| None | **Birds Only (97.21%)** | Non-avian records (iNaturalist, museums) have `eventID = None`. |
| **Checklist Grouping Feasibility?**| **IMPOSSIBLE** | **FEASIBLE** | Occurrences with identical `eventID` share exact date, time, and coordinates. |
| **`samplingProtocol`?** | **NO** | **YES in header (Null)** | Uniformly `None` across eBird records in GBIF. |
| **Survey Effort (Duration, Distance)**| **NO** | **NO** (`None`) | Ingested eBird data in GBIF does not provide effort minutes or km. |
| **Complete Checklist Flag?** | **NO** | **NO** | `all_species_reported` flag is NOT passed from eBird to GBIF. |
| **Non-Detections (Absences)?** | **NO (100% PRESENT)** | **NO (100% PRESENT)** | Neither format contains non-detections or true absences. |
| **Compressed Size** | ~995 MB | ~1.8 GB | Both fit easily within available 435 GiB storage (<1.6%). |
| **Uncompressed Size** | ~3.5 GB (Single flat file) | ~7.0 GB (Relational archive) | `SIMPLE_CSV` loads faster; `DWCA` requires unzipping. |

---

### Empirical Verification of Checklist Grouping:
1. **Linking Occurrences**: In `DWCA`, individual occurrence records sharing the same `eventID` represent individual species sightings recorded during the same observer visit. For example, checklist `S159345450` in Bengaluru links 63 distinct bird species records observed on `2024-01-20` at Lat $13.068254^\circ\text{ N}$, Lon $77.560549^\circ\text{ E}$.
2. **Identifier Consistency**: In eBird, `eventID` is structured as `S` followed by 7 to 9 digits. It is unique per submitted checklist within the eBird system.
3. **Absence of Effort Variables**: While checklist-level grouping is feasible without inventing data, GBIF DWCA does **not** provide duration (minutes), distance traveled (km), survey protocol (stationary, traveling, incidental), or the complete checklist flag (`all_species_reported`).
4. **Taxonomic Asymmetry**: Because `eventID` is only populated for eBird, checklist clustering is restricted to Class Aves (birds). The remaining 108,856 records (iNaturalist observations of insects, mammals, reptiles, amphibians, plants) lack `eventID` and cannot be clustered into checklists.

---

## 4. Feasibility Assessment & Rarefaction Indicator Downgrade

### Quantitative Assessment of Sampling Units:
- **Distinct Event IDs by Landscape (2012–2024 Clean)**:
  - **Bengaluru**: $\approx 110,000 - 130,000$ eBird checklists (from 2,864,385 bird records; 97.19% of regional data).
  - **Mysuru**: $\approx 30,000 - 35,000$ eBird checklists (from 743,539 bird records; 97.59% of regional data).
  - **Nilgiri–Bandipur**: $\approx 7,000 - 9,000$ eBird checklists (from 184,240 bird records; 96.04% of regional data).
- **Missing Event IDs**: Across all three landscapes, exactly **108,856 records (2.79%)** have `eventID = None`. These comprise all non-avian biodiversity.
- **Spatial Inequality of Events**:
  - Spatial sampling inequality is extreme (Gini coefficients: BLR = **0.7276**, MYS = **0.7868**, NB = **0.8240**).
  - While urban birding hotspots contain >10,000 checklists, rural and forest cells have very few.
  - In Nilgiri-Bandipur, the median cell has only **$\sim 16$ checklists across 13 years** ($\sim 1.2$ checklists/year), and cell `NB_R10_C04` has **0 checklists**.
- **Incomparability of Sampling Units**:
  - In citizen science, an eBird checklist is not a standardized ecological quadrat. One checklist may represent a 5-minute opportunistic garden observation, while another represents a 5-hour, 12-km expedition by a team of expert ornithologists.
  - Without duration and distance metrics, rarefying to a fixed number of checklists treats fundamentally disparate observation efforts as equivalent.

---

### Indicator Feasibility Matrix (Re-evaluated)

| Candidate Biodiversity Indicator | GBIF Support Status | Required Fields | Inherent Biases & Critical Limitations | Role in DEI Research |
| :--- | :---: | :--- | :--- | :--- |
| **1. Observed Richness ($S_{obs}$)** | **SUPPORTED (DESCRIPTIVE ONLY)** | `speciesKey`, coordinates | Severe observer effort bias ($r > 0.85$ with checklist count) | **Descriptive baseline only**; must use checklist count as covariate |
| **2. Sample-Based Rarefaction** | **EXPLORATORY / CONDITIONAL (BIRDS ONLY)** | `speciesKey`, `eventID`, coords | • **Birds only** (non-avian taxa lack `eventID`)<br>• Checklists vary widely in duration/distance<br>• Fails in sparse cells (<10 checklists) | **Downgraded to exploratory**; usable only for comparative avifaunal analysis in high-effort cells |
| **3. Species Occurrence Frequency ($f_i$)** | **SUPPORTED WITH CAVEATS** | `speciesKey`, `eventDate`, coords | Reflects detectability and species popularity | Moderate; feasible at annual aggregation for common taxa |
| **4. Species Turnover ($\beta$-diversity)** | **CONDITIONAL / LIMITED** | `speciesKey`, coordinates | Heavily confounded by unequal sampling effort between compared cells | Comparative only across cell pairs with matched checklist volumes |
| **5. Occupancy Estimation ($\psi$)** | **NOT SUPPORTED** | Detection / non-detection matrix | 100% presence-only; zero non-detections; complete checklist flag missing | **DO NOT USE (Prohibited; pseudo-absences violate Zero Synthetic Data)** |
| **6. Absolute Abundance ($N$)** | **STRICTLY PROHIBITED** | Standardized transect counts | `individualCount` missing in >98% of records; repeat counts inflate totals | **STRICTLY PROHIBITED (Raw sightings $\neq$ abundance)** |
| **7. Population Density ($D$)** | **STRICTLY PROHIBITED** | Absolute counts, census area | Presence-only point observations cannot infer biological density | **STRICTLY PROHIBITED** |

---

## 5. Formal Format Recommendation and Justification

### Formal Format Recommendation: **`DWCA` (Darwin Core Archive)**

1. **Why `DWCA` is Recommended**:
   - `DWCA` is the **only** GBIF format that preserves **`eventID`**.
   - Preserving `eventID` is mandatory to cluster individual species records into checklists. Even though sample-based rarefaction is downgraded to exploratory, retaining `eventID` allows bird-specific checklist clustering, observer visit counts, and effort-standardized species accumulation analyses.
   - In contrast, `SIMPLE_CSV` permanently strips `eventID`, destroying all sampling event cohesion.
2. **What `DWCA` Actually Preserves**:
   - Preserves 230 interpreted fields in `occurrence.txt` (including `gbifID`, `eventID`, `datasetKey`, `scientificName`, `decimalLatitude`, `decimalLongitude`, `eventDate`, `year`, `basisOfRecord`, `catalogNumber`).
   - For eBird records (97.21% of the archive), `eventID` contains the unique checklist identifier (`S...`).
3. **What `DWCA` Does NOT Preserve**:
   - It does **not** preserve survey duration (minutes), distance traveled (km), observer number, or protocol description (all are `None`).
   - It does **not** preserve the complete checklist flag (`all_species_reported`).
   - It does **not** contain non-detections or true absences (`occurrenceStatus` is 100% `PRESENT`).
4. **Computational Feasibility**:
   - Compressed size: ~1.8 GB. Uncompressed size: ~7.0 GB.
   - The local environment has **435 GiB of free disk space**, so `DWCA` consumes less than **1.6%** of available capacity.
   - Downstream ingestion will parse `occurrence.txt` using chunked streaming in Python (`polars` or `pandas`), extracting only the necessary columns.

---

## 6. Final Validated Predicate Specification

```json
{
  "creator": "<gbif_username>",
  "notificationAddresses": ["<user_email>"],
  "sendNotification": true,
  "format": "DWCA", 
  "predicate": {
    "type": "and",
    "predicates": [
      {
        "type": "greaterThanOrEquals",
        "key": "YEAR",
        "value": "2012"
      },
      {
        "type": "lessThanOrEquals",
        "key": "YEAR",
        "value": "2024"
      },
      {
        "type": "equals",
        "key": "HAS_COORDINATE",
        "value": "true"
      },
      {
        "type": "equals",
        "key": "HAS_GEOSPATIAL_ISSUE",
        "value": "false"
      },
      {
        "type": "or",
        "predicates": [
          {
            "type": "within",
            "geometry": "POLYGON ((77.817859 12.739603, 77.822948 13.191189, 77.361986 13.195857, 77.357725 12.744105, 77.817859 12.739603))"
          },
          {
            "type": "within",
            "geometry": "POLYGON ((76.883407 12.079049, 76.886631 12.530962, 76.426593 12.533799, 76.424155 12.081780, 76.883407 12.079049))"
          },
          {
            "type": "within",
            "geometry": "POLYGON ((76.824013 11.428614, 76.826965 11.880564, 76.368036 11.883159, 76.365825 11.431108, 76.824013 11.428614))"
          }
        ]
      }
    ]
  }
}
```

### Certified Target Counts:
- **Bengaluru**: **2,947,292 records** (2 excluded for geospatial issues)
- **Mysuru**: **761,890 records** (1 excluded for geospatial issues)
- **Nilgiri–Bandipur**: **191,838 records** (0 excluded)
- **Total Combined Download Target**: **3,901,020 clean records**

---

## 7. Compliance with Stopping Rules

1. **No Bulk Download Initiated**: No download request has been submitted to `api.gbif.org/v1/occurrence/download/request`. No bulk occurrence files were downloaded.
2. **Zero Credentials in Files**: No usernames, passwords, or personal email addresses have been stored or hardcoded in any script, report, notebook, or git record.
3. **Zero Synthetic Data / No Pseudo-Absences**: No coordinates, sightings, or artificial absences were fabricated.
4. **No Boundary Modifications**: All three approved 50 km × 50 km study boundaries and 300 5 km grid cells remain strictly unchanged.
5. **Strict Scope Control**: No work has been performed on GloBI, ESA WorldCover, or predictive neural network models.
6. **No Git Push**: Repository remains strictly local.

---

## 8. Final Audit Sign-Off

# **VERDICT: READY FOR APPROVAL**

The audit is complete. All 5 check items have been comprehensively addressed:
- The 561 unassigned Bengaluru records are mathematically proven as geodetic chord curvature slivers and handled cleanly via `outside_grid_assignment`.
- Bandipur cell `NB_R10_C04` is properly documented as human observer effort deficiency rather than ecological absence.
- The `DWCA` specification and eBird `eventID` structure are verified.
- Rarefaction feasibility has been rigorously evaluated and downgraded to exploratory for birds.
- The pipeline stands ready for user authorization to launch the registered download.
