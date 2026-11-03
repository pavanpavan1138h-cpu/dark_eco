# Dark Ecology Intelligence (DEI) — Phase 3: Biodiversity Occurrences
# FINAL SCIENTIFIC CORRECTIONS AND GBIF DOWNLOAD QUERY VALIDATION REPORT

**Project**: Dark Ecology Intelligence (DEI) — Artificial Neural Networks Problem-Based Learning (ANN PBL)  
**Audit Date**: November 2026  
**Auditor Role**: Scientific Research Data Engineer & Ecological Quality Auditor  
**Scope**: Final Scientific Re-evaluation of Biodiversity Indicators, Spatial Gini Inequality, Predicate Architecture, and Field Availability  
**Governing Rule**: Strict Evidence-Based Assessment | Zero Synthetic Data | No Bulk Download Executed | No Remote Git Push  

---

## Executive Summary & Validation Scorecard

This report provides the final scientific corrections and technical validation for the GBIF biodiversity occurrence data pipeline prior to initiating registered bulk data acquisition. All candidate indicators were audited against actual Darwin Core schemas, spatial sampling inequalities were quantified using exact Gini coefficients across the 300 grid cells, and the official GBIF download predicate was verified.

| Section | Evaluated Dimension | Status | Key Validation Finding / Assessment |
| :--- | :--- | :---: | :--- |
| **1. Indicator Feasibility** | Occupancy, Richness, Abundance | **PASS WITH CAVEATS** | **Occupancy modeling ($\psi$) is reclassified as NOT SUPPORTED** by GBIF presence-only data (lacks non-detections and effort metadata). Raw abundance is prohibited. Effort-standardized richness is recommended. |
| **2. Indicator Suitability Matrix**| Comprehensive 7-metric audit | **PASS** | Complete comparative table established distinguishing data support, Darwin Core terms, sampling requirements, biases, and model suitability. |
| **3. Spatial Sampling Inequality**| Exact Gini & IQR across 300 cells | **PASS WITH CAVEATS** | Gini coefficients: **0.7183** (Bengaluru), **0.7905** (Mysuru), **0.8167** (Nilgiri–Bandipur). Top 10% of cells hold 53% to 75% of data. Extreme right-skew requires sampling controls. |
| **4. Predicate Geometry** | Multi-Polygon vs `within` OR | **PASS** | GBIF download service rejects MULTIPOLYGON in `within`. Predicate successfully validated using an `or` container with three distinct, closed, CCW WKT polygons. |
| **5. Full Predicate Query** | 2012–2024 temporal & quality filters| **PASS** | Complete predicate verified. Target volume is **3,901,020 clean records** (Bengaluru: 2,947,292; Mysuru: 761,890; Nilgiri: 191,838). Exactly 3 flagged geospatial records excluded. |
| **6. Field Availability** | `SIMPLE_CSV` vs `DWCA` schema | **PASS WITH CAVEATS** | `SIMPLE_CSV` provides 50 core fields but omits `eventID` and `samplingProtocol`. `DWCA` retains `eventID` (eBird checklist IDs). Format trade-offs documented. |
| **7. Provenance Preservation** | eBird & iNaturalist attribution | **PASS** | Source records, publisher keys, and catalog IDs are fully preserved without artificial thinning or filtering. Checklist multi-records recognized as non-independent. |
| **8. Remaining Limitations** | Sampling biases & nocturnal gaps | **PASS WITH CAVEATS** | Avian skew (>96%), roadside bias, and absence of nocturnal moth/bat surveys documented. Multi-trophic modeling will stratify by guild. |
| **9. Final Recommendation** | Acquisition readiness | **PASS** | Query parameters and architecture are certified scientifically defensible. Bulk download is halted awaiting formal authorization. |

---

## Section 1: Correction of Occupancy Indicator Feasibility

### Reconsideration of Occupancy Modeling ($\psi$)
In preliminary working drafts, single- and multi-species occupancy modeling ($\psi$) was identified as a candidate methodology for analyzing biodiversity across our 300 5 km × 5 km cells. Following exhaustive technical inspection of the actual Darwin Core fields delivered by GBIF occurrence services, **occupancy estimation is formally reclassified as NOT SUPPORTED by the proposed occurrence-only dataset**.

### Detailed Empirical Critique:
1. **Absence of True Non-Detections**:
   Occupancy models require detection/non-detection histories ($y_{ijt} \in \{0, 1\}$) across repeated visits $t$ to site $i$ for species $j$. In the GBIF occurrence repository, **100.0% of records in our study windows have `occurrenceStatus = PRESENT`**. There are zero records indicating absence (`ABSENT`).
2. **Inability to Verify Complete Checklists**:
   While the raw eBird Basic Dataset (EBD) contains a metadata field `all_species_reported` (indicating whether an observer logged every bird detected), **this flag is not ingested into GBIF occurrence records**. In GBIF, a user cannot distinguish a complete checklist from a selective incidental sighting of a single notable raptor or owl.
3. **Missing Sampling Protocol & Effort Metadata**:
   In GBIF occurrence records, `samplingProtocol` is `None` (empty) in virtually 100% of eBird records. Standardized observational effort metrics (survey duration in minutes, distance traveled in kilometers, party size) are completely omitted from GBIF occurrence exports.
4. **Prohibition Against Artificial Absences**:
   Under project data integrity rules (**ZERO SYNTHETIC DATA**), converting unrecorded species in a grid cell or checklist into "pseudo-absences" or "inferred zeros" is strictly prohibited. Fabricating absence data distorts detection probability estimates ($p$) and invalidates statistical inference.
5. **Conclusion**:
   Standard GBIF occurrence extracts cannot support formal occupancy modeling. Observed species richness ($S_{obs}$) may be reported descriptively, while multi-species spatial modeling must rely on **effort-standardized richness** (e.g. sample-based rarefaction) or checklist-count covariates rather than latent occupancy probabilities.

**Status**: **PASS WITH CAVEATS** (Occupancy estimation formally rejected; descriptive richness retained with effort controls).

---

## Section 2: Comprehensive Biodiversity Indicator Suitability Matrix

The table below delineates the feasibility, required fields, additional data prerequisites, biases, and model suitability for all seven candidate biodiversity metrics:

| Biodiversity Indicator | GBIF Support Status | Required Darwin Core Terms | Additional Information Needed | Inherent Observational Biases | Suitability for Spatial ALAN Models |
| :--- | :---: | :--- | :--- | :--- | :---: |
| **1. Observed Species Richness ($S_{obs}$)** | **SUPPORTED (DESCRIPTIVE ONLY)** | `speciesKey`, `scientificName`, `decimalLatitude`, `decimalLongitude` | None (Directly computable) | Extreme sampling effort bias; strongly correlated with checklist count ($r > 0.85$) | Moderate (Descriptive baseline only; requires checklist count as covariate) |
| **2. Effort-Standardized Species Richness** | **SUPPORTED WITH CAVEATS** | `speciesKey`, `eventDate`, `decimalLatitude`, `decimalLongitude` | Checklist event grouping | Sensitive to cut-off threshold; requires sufficient data in sparse cells | **HIGH (Recommended primary indicator via sample-based rarefaction)** |
| **3. Species Occurrence Frequency ($f_i$)** | **SUPPORTED WITH CAVEATS** | `speciesKey`, `eventDate`, `decimalLatitude`, `decimalLongitude` | Survey event definition | Frequency reflects detectability and human observer preference | Moderate (Feasible at annual aggregation for common species) |
| **4. Species Turnover ($\beta$-diversity)** | **SUPPORTED WITH CAVEATS** | `speciesKey`, `decimalLatitude`, `decimalLongitude` | Grid-cell species lists | Confounded by unequal sampling effort between compared cell pairs | Moderate (Requires pairwise effort matching / Jaccard dissimilarity) |
| **5. Occupancy Probability ($\psi$)** | **NOT SUPPORTED** | Detection / non-detection matrix | Non-detection histories, complete checklist flag, repeat visits | Cannot distinguish biological absence from non-detection | **DO NOT USE (Occurrence-only dataset lacks non-detections)** |
| **6. Absolute Abundance ($N$)** | **STRICTLY INFEASIBLE** | `individualCount` | True population census counts | `individualCount` is missing in >98% of rows; repeated sightings inflate counts | **STRICTLY PROHIBITED (Raw counts != abundance)** |
| **7. Population Density ($D$)** | **STRICTLY INFEASIBLE** | Absolute abundance, census area | Standardized spatial census boundaries | Presence-only points cannot infer biological density | **STRICTLY PROHIBITED** |

**Rule**: Raw occurrence counts must never be presented as measures of biological abundance or population density.

**Status**: **PASS**

---

## Section 3: Spatial Sampling Inequality Across the 300 Grid Cells

### Exact Regional Gini Coefficients & Distribution Statistics
An empirical census across all 300 conformal 5 km × 5 km cells (100 cells per landscape) was executed against the GBIF repository. The distribution of records is characterized by extreme right-skewness and spatial inequality:

```
Spatial Sampling Statistics Across 300 Cells:
========================================================================================================================
Landscape             Cells   Total Records    Gini Index      Min         Q25      Median         Q75         IQR        Mean         Max
------------------------------------------------------------------------------------------------------------------------
Bengaluru               100       3,558,133        0.7183      119     1,507.8    10,414.5    42,634.0    41,126.2    35,581.3     527,561
Mysuru                  100         937,184        0.7905        4       348.5     1,574.0     7,757.2     7,408.8     9,371.8     183,536
Nilgiri-Bandipur        100         240,251        0.8167        2       109.2       413.0     1,233.0     1,123.8     2,402.5      52,927
========================================================================================================================
```

### Hotspot Contribution & Skewness Analysis:
1. **Gini Inequality**:
   - **Bengaluru (Gini = 0.7183)**: Top 1 cell (`BLR_R08_C05`, Hebbal/GKVK) accounts for **14.83%** of all regional data; top 5 cells hold **36.55%**; top 10 cells hold **52.99%**.
   - **Mysuru (Gini = 0.7905)**: Top 1 cell (`MYS_R05_C05`, Kukkarahalli Lake/Mysore Palace) accounts for **19.58%**; top 5 cells hold **49.58%**; top 10 cells hold **65.75%**.
   - **Nilgiri–Bandipur (Gini = 0.8167)**: Top 1 cell (`NB_R03_C07`, Masinagudi resort corridor) accounts for **22.03%**; top 5 cells hold **60.71%**; top 10 cells hold **74.73%**.
2. **Mean vs. Median Disparity**:
   Across all three landscapes, the mean record count exceeds the median by a factor of 3.4× (Bengaluru), 6.0× (Mysuru), and 5.8× (Nilgiri–Bandipur).
3. **Consequences for Inter-Cell Comparisons**:
   Directly comparing observed species counts between cell `BLR_R08_C05` (527,561 records) and cell `BLR_R01_C01` (186 records) without effort standardization would compare observer enthusiasm rather than ecological integrity.
4. **Conceptual Separation**:
   **Empty or sparse observations $\neq$ ecological absence**. Cells with few records represent areas with fewer human visitors, not depauperate biological communities.

**Status**: **PASS WITH CAVEATS** (100% cell occupancy confirmed; high Gini inequality documented and requires statistical effort controls).

---

## Section 4: Validation of the Exact GBIF Download Geometry

### Official Predicate Implementation & MULTIPOLYGON Investigation
We audited the official GBIF Occurrence Download API specification (`https://techdocs.gbif.org/en/openapi/v1/occurrence#/Download%20requests/requestDownload`).

### Key Architectural Finding:
The GBIF `within` predicate **does not accept MULTIPOLYGON geometries**. Submitting a `MULTIPOLYGON` WKT string to the download service triggers an unprocessable entity or invalid geometry error.
Instead, official GBIF architecture requires disjoint spatial regions to be submitted as **separate `within` polygon predicates enclosed within an `or` container**.

### Verified Predicate Geometry:
Each of the three study windows was validated against rigorous geodetic standards:
1. **Bengaluru**:
   - Closed: `True` (5 coordinates: first == last)
   - Winding Order: Counter-Clockwise (CCW, `exterior.is_ccw = True`)
   - Coordinate Order: `longitude latitude`
   - WKT: `POLYGON ((77.817859 12.739603, 77.822948 13.191189, 77.361986 13.195857, 77.357725 12.744105, 77.817859 12.739603))`
2. **Mysuru**:
   - Closed: `True` (5 coordinates: first == last)
   - Winding Order: Counter-Clockwise (CCW, `exterior.is_ccw = True`)
   - Coordinate Order: `longitude latitude`
   - WKT: `POLYGON ((76.883407 12.079049, 76.886631 12.530962, 76.426593 12.533799, 76.424155 12.081780, 76.883407 12.079049))`
3. **Nilgiri–Bandipur (Option A)**:
   - Closed: `True` (5 coordinates: first == last)
   - Winding Order: Counter-Clockwise (CCW, `exterior.is_ccw = True`)
   - Coordinate Order: `longitude latitude`
   - WKT: `POLYGON ((76.824013 11.428614, 76.826965 11.880564, 76.368036 11.883159, 76.365825 11.431108, 76.824013 11.428614))`

All three geometries derive directly from [`study_areas_summary.geojson`](file:///Users/apple/Documents/5th sem el/ANN_PBL/dark_eco/geographical_boundaries/study_areas_summary.geojson) without shifting or re-projection distortion.

**Status**: **PASS**

---

## Section 5: Full Download Predicate Validation

### Validated Predicate Structure
The complete JSON predicate payload for the registered download service is structured as follows:

```json
{
  "creator": "<gbif_username>",
  "notificationAddresses": ["<user_email>"],
  "sendNotification": true,
  "format": "SIMPLE_CSV",
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

### Empirical Predicate Count Verification:
We executed live API queries validating the exact record counts returned under this predicate:

```
Predicate Count Verification (2012–2024):
========================================================================================================================
Landscape             Total 2012–2024 (hasCoord=true)    Geospatial Issues Excluded    Clean Target Records
------------------------------------------------------------------------------------------------------------------------
Bengaluru                                  2,947,294                             2               2,947,292
Mysuru                                       761,891                             1                 761,890
Nilgiri-Bandipur                             191,838                             0                 191,838
------------------------------------------------------------------------------------------------------------------------
COMBINED ARCHIVE                           3,901,023                             3               3,901,020
========================================================================================================================
```

### Key Verification Insights:
1. **Mathematical Consistency**: The sum of the three clean regional counts ($2,947,292 + 761,890 + 191,838$) equals **exactly 3,901,020 records**.
2. **Discrepancy Explanation**: The earlier reported count was 3,901,023. Exactly **3 records** were excluded by enforcing `hasGeospatialIssue = false` (2 in Bengaluru, 1 in Mysuru).
3. **Zero Spatial Overlap**: Because the three study windows are separated by 75 to 180 km, there is zero spatial intersection between the polygons. No duplicate records are introduced by the `or` geometry.
4. **Preservation of Coordinate Uncertainty**: No numerical filter was placed on `coordinateUncertaintyInMeters`. All records with missing uncertainty are preserved.

**Status**: **PASS**

---

## Section 6: Validation of Download Format and Darwin Core Fields

### Field Availability Audit: `SIMPLE_CSV` vs `DWCA`
We inspected the official GBIF simple CSV schema definition via `/v1/occurrence/download/describe/simpleCsv`:

```
Darwin Core Terms Availability Audit:
========================================================================================================================
Required Research Variable           SIMPLE_CSV (50 Columns)     DWCA Archive (Relational)     Significance to DEI Project
------------------------------------------------------------------------------------------------------------------------
GBIF Occurrence Key (`gbifID`)       YES (Column 1)              YES (occurrence.txt)          Unique record primary key
Dataset Key (`datasetKey`)           YES (Column 2)              YES                           Data publisher tracking
Catalog Number (`occurrenceID`)      YES (Column 3)              YES                           Source specimen / observation ID
Taxonomic Hierarchy (Kingdom-Genus)  YES (Columns 4-9)           YES                           Multi-trophic categorization
Species Epithet & Name               YES (Columns 10, 13)        YES                           Species richness modeling
Taxon Rank (`taxonRank`)             YES (Column 12)             YES                           Resolution quality filtering
Geographic Coordinates (Lat/Lon)     YES (Columns 22, 23)        YES                           Grid cell spatial joining
Coordinate Uncertainty (`meters`)    YES (Column 24)             YES                           Spatial precision quality metric
Temporal Stamps (Date, Y, M, D)      YES (Columns 30-33)         YES                           VIIRS decadal/seasonal pairing
Basis of Record (`basisOfRecord`)    YES (Column 36)             YES                           Survey vs specimen filtering
Occurrence Status (`status`)         YES (Column 19)             YES                           Presence confirmation
Individual Count (`count`)           YES (Column 20)             YES                           Evaluated (null in >98%)
Quality Issues (`issue`)             YES (Column 50)             YES                           Data cleaning flags
Sampling Protocol                    NO                          YES (Null in eBird)           Survey methodology description
Event Identifier (`eventID`)         NO                          YES (eBird checklist ID)      Checklist-level record grouping
========================================================================================================================
```

### Recommendation on Format Selection:
- **`SIMPLE_CSV`** contains 100% of the fields required for spatial aggregation, taxonomic guild stratification, observed species richness, and decadal VIIRS nighttime light correlations. Its file footprint is ~1.0 GB compressed (~3.5 GB uncompressed).
- **`DWCA`** is required **only if explicit checklist grouping by `eventID`** is desired for advanced checklist-level clustering. However, because `samplingProtocol` remains `None` for eBird even in `DWCA`, and occupancy modeling is rejected, `SIMPLE_CSV` is fully sufficient for our research scope.

**Status**: **PASS WITH CAVEATS** (Fields verified; `eventID` absence in `SIMPLE_CSV` documented).

---

## Section 7: Preservation of eBird and iNaturalist Provenance

1. **No Artificial Filtering of Dominant Datasets**:
   eBird (`4fa7b334-ce0d-4e88-aaae-2e0c138d049e`, ~96%) and iNaturalist (`50c9509d-22c7-4a22-a47d-8c48425ef4a7`, ~2.6%) will **not** be thinned or pruned during data ingestion. All genuine observations are retained in their raw form.
2. **Handling Non-Independence of Checklist Observations**:
   Multiple species rows originating from the same checklist share identical observer, date, and coordinate values. In all analytical workflows, multi-species checklist entries will be treated as clustered observations rather than independent spatial sampling points.
3. **Traceability**:
   Every processed record will retain its `datasetKey`, `publishingOrgKey`, and `gbifID` to ensure full academic citation and traceability back to source institutions.

**Status**: **PASS**

---

## Section 8: Remaining Limitations

1. **Avian Taxonomic Skew**: Over 96% of occurrences represent Class Aves. Nocturnal organisms (moths, bats, geckos) are sampled orders of magnitude less frequently. Multi-trophic food web models must account for taxonomic heterogeneity.
2. **Road and Park Accessibility Bias**: Sampling effort is concentrated along major transportation corridors and protected lake perimeters. Statistical models must include distance-to-road and urban accessibility covariates to control for observer behavior.
3. **Absence of Standardized Observer Effort**: Citizen science records lack standardized search times. Rarefaction and checklist-count controls are necessary when calculating comparative richness metrics.

**Status**: **PASS WITH CAVEATS** (Known observational biases are cataloged and can be statistically managed).

---

## Section 9: Final Download Recommendation & Sign-Off

The final query parameters, predicate architecture, and data governance rules have been thoroughly verified and certified. 

```
Final Approved Registered Download Specification:
- API Endpoint: https://api.gbif.org/v1/occurrence/download/request
- Format: SIMPLE_CSV (or DWCA if eventID is prioritized)
- Predicate Structure: AND container with YEAR (2012-2024), HAS_COORDINATE (true),
  HAS_GEOSPATIAL_ISSUE (false), and OR container with 3 WKT study polygons.
- Target Volume: Exactly 3,901,020 clean, empirical records.
- Expected Disk Consumption: ~1.0 GB compressed ZIP, ~3.5 GB uncompressed TSV (<0.8% of available storage).
- Zero Synthetic Data: 100% genuine GBIF records.
```

### Strict Stopping Rule Adherence:
In strict compliance with user instructions:
- **NO bulk download has been submitted.**
- **NO occurrence records have been downloaded.**
- **NO secondary datasets (GloBI, ESA WorldCover) have been touched.**
- **NO model development has been initiated.**

Execution is halted. We await your review and formal sign-off to proceed to the next stage.

