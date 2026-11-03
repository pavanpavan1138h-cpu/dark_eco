# Final Phase 1 Scope & Quality Audit Report
**Project: Dark Ecology Intelligence (DEI) — ANN PBL**
**Date of Audit: 2026-11-03**
**Scope: Four Core Datasets Only (VIIRS-DNB, GBIF, GloBI, ESA WorldCover)**

---

## 1. Executive Summary & Audit Overview

In accordance with user instructions, the research scope for the initial collection and modeling pipeline is **strictly frozen to four core datasets**:
1. **VIIRS-DNB** (Nighttime Light / ALAN)
2. **GBIF** (Biodiversity Occurrence Records)
3. **GloBI** (Ecological Trophic Interactions)
4. **ESA WorldCover** (10m Land Cover Baseline)

All other 23 candidate datasets catalogued during Phase 1 (such as DMSP-OLS, NASA Black Marble, eBird, Mangal, EltonTraits, AVONET, Hansen GFC, WorldPop, GHSL, ERA5-Land, Copernicus DEM) remain strictly frozen as optional secondary references and **will not be downloaded or ingested** without explicit authorization.

This audit evaluates the spatial integrity of the three study windows, performs empirical quality probes on GBIF and GloBI, verifies access endpoints for VIIRS-DNB and ESA WorldCover, and certifies zero synthetic research data.

---

## 2. Audit Status Summary

| Audit Item | Status | Key Evidence / Metric |
| :--- | :---: | :--- |
| **1. Four-Dataset Scope Freeze** | `VERIFIED` | Pipeline locked to VIIRS-DNB, GBIF, GloBI, ESA WorldCover; others marked optional reference only. |
| **2. Geographical Windows (50 km × 50 km)** | `VERIFIED` | Exact 2,500 km² windows; Bengaluru, Mysuru, Nilgiri-Bandipur delineated without overlap. |
| **3. Spatial Grid (5 km × 5 km)** | `VERIFIED` | 100 cells/window = 300 cells total; each cell is exactly 25.0 km² in UTM Zone 43N. |
| **4. CRS Suitability (UTM Zone 43N)** | `VERIFIED` | Scale distortion strictly between -0.04% and +0.075% (<0.08% maximum error); fully conformal and metric. |
| **5. Nilgiri–Bandipur Boundary Delineation** | `REQUIRES USER DECISION` | Current window captures 74.6% of Bandipur+Mudumalai OSM area; sliding 15km W, 10km N reaches 87.5% but excludes Nilgiri slopes. |
| **6. GBIF Data Quality (Coordinates & Dates)** | `VERIFIED` | >98.6% of records have valid coordinates and usable dates (1992–2024); total records >4.7M across 3 regions. |
| **7. GBIF Coordinate Uncertainty Reporting** | `PARTIALLY VERIFIED` | Only 2.4%–3.6% of GBIF records include explicit `coordinateUncertaintyInMeters` (due to eBird checklist defaults). |
| **8. GloBI Regional Interaction Availability** | `PARTIALLY VERIFIED` | Abundant species-pair interaction records exist for regional taxa, but ~0% have direct field GPS coordinates or dates. |
| **9. VIIRS-DNB Data Access Readiness** | `VERIFIED` | EOG VNL v2.2 endpoint verified; regional tile Tile 3 (00N–75N, 060E–120E) covers all 3 study windows. |
| **10. ESA WorldCover Access Readiness** | `VERIFIED` | Only two 3°×3° tiles (`N12E075`, `N09E075`) cover all three study areas; public AWS S3 COG endpoints verified (HTTP 200). |
| **11. Zero Synthetic Research Data Audit** | `VERIFIED` | Zero random, synthetic, dummy, or fabricated records exist across all project directories. |

---

## 3. Geographical Boundaries & Grid Verification

### 3.1 Study Area Envelopes & Centroids

| Landscape Window | Centroid (WGS 84) | Latitude Bounds (WGS 84) | Longitude Bounds (WGS 84) | UTM Zone 43N Bounds (m) | Total Area |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Bengaluru Urban-Periurban** | 12.9716° N, 77.5946° E | 12.7396° N – 13.1959° N | 77.3577° E – 77.8229° E | E: 756,000–806,000; N: 1,410,000–1,460,000 | 2,500 km² |
| **Mysuru Peri-Urban/Transitional** | 12.3051° N, 76.6551° E | 12.0790° N – 12.5338° N | 76.4242° E – 76.8866° E | E: 655,000–705,000; N: 1,336,000–1,386,000 | 2,500 km² |
| **Nilgiri–Bandipur Forest Corridor** | 11.6600° N, 76.6000° E | 11.4286° N – 11.8832° N | 76.3658° E – 76.8270° E | E: 649,000–699,000; N: 1,264,000–1,314,000 | 2,500 km² |

### 3.2 5 km × 5 km Spatial Grid Properties
- **Total Cell Count**: Exactly 300 cells (100 cells per landscape, organized in a 10 × 10 regular lattice).
- **Metric Area**: Every cell has an exact area of **25.000 km²** in UTM Zone 43N ($5,000\text{ m} \times 5,000\text{ m}$).
- **Identifiers**: Deterministic IDs (`BLR_R01_C01` to `BLR_R10_C10`, `MYS_R01_C01` to `MYS_R10_C10`, `NB_R01_C01` to `NB_R10_C10`).
- **GeoJSON Integrity**: All boundary and grid files in `geographical_boundaries/` adhere strictly to RFC 7946 (WGS 84 coordinate order: `[longitude, latitude]`).

### 3.3 Coordinate Reference System (CRS) Distortion Audit
- **Projected CRS**: WGS 84 / UTM Zone 43N (`EPSG:32643`).
- **Central Meridian**: 75°00' E.
- **Longitude Range of Study System**: 76°21' E to 77°50' E (distance from central meridian: $1.36^\circ$ to $2.82^\circ$).
- **Scale Factor Analysis**:
  - At central meridian: $k = 0.9996$ (-0.04% linear compression).
  - At Mysuru / Nilgiri-Bandipur ($X \approx 650,000\text{ m}$): $k \approx 0.99988$ (-0.012% linear distortion).
  - At Eastern Bengaluru ($X \approx 806,000\text{ m}$): $k \approx 1.00075$ (+0.075% linear dilation).
- **Verdict**: **`VERIFIED`**. Maximum linear distortion across the entire three-region study domain is less than 0.08% (80 cm per km). This is far below any ecological modeling significance threshold.

### 3.4 Outstanding Decision: Nilgiri–Bandipur Boundary Window
- **Finding**: The current 50 km × 50 km window captures **99.9% of Mudumalai NP** (335.6 km²) and **65.6% of Bandipur NP** (622.4 km²), totaling 958.0 km² (74.6% of their combined area). It includes the critical Masinagudi corridor and Gundlupet agricultural fringe while keeping Ooty town outside (1.8 km beyond the southern border).
- **Alternative**: Shifting the window 15 km West and 10 km North increases protected area coverage to **87.5% (1,123.8 km²)**, but reduces coverage of the Sigur Plateau / Masinagudi human-wildlife interface.
- **Status**: **`REQUIRES USER DECISION`**. The current window is preserved pending explicit user instruction.

---

## 4. GBIF Biodiversity Occurrence Quality Audit

Using live queries against the official GBIF Occurrence API (`https://api.gbif.org/v1/occurrence/search`) across each landscape's bounding box, the empirical record counts and quality attributes were audited:

| Region | Total Records | With Valid Coordinates | Usable Dates (1992–2024) | With Uncertainty Stated | Uncertainty $\le 1000\text{ m}$ | Geospatial Issues | Top Taxonomic Classes |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Bengaluru** | 3,562,914 | 3,562,914 (100%) | 3,556,453 (99.8%) | 99,092 (2.8%) | 86,137 (2.4%) | 11 (<0.001%) | Aves: 3,470,032; Insecta: 49,457; Magnoliopsida: 28,530; Arachnida: 6,254 |
| **Mysuru** | 937,355 | 937,355 (100%) | 934,886 (99.7%) | 22,174 (2.4%) | 17,667 (1.9%) | 2 (<0.001%) | Aves: 920,971; Insecta: 9,619; Magnoliopsida: 3,726; Arachnida: 1,198 |
| **Nilgiri–Bandipur** | 240,918 | 240,918 (100%) | 237,532 (98.6%) | 8,784 (3.6%) | 5,001 (2.1%) | 5 (<0.001%) | Aves: 233,012; Mammalia: 2,429; Insecta: 2,350; Magnoliopsida: 1,928 |

### Key Quality Findings:
1. **Taxonomic Skew**: Over 95% of records across all three regions are birds (`classKey: 212`, Aves), primarily ingested from eBird citizen science checklists.
2. **Coordinate Uncertainty Limitation**: Only 2.4% to 3.6% of records contain explicit numerical values in `coordinateUncertaintyInMeters`. This occurs because standard eBird checklist uploads do not require observers to supply a positional uncertainty radius. 
   - *Mitigation for Phase 3*: We cannot simply filter on `coordinateUncertaintyInMeters <= 1000` because doing so would eliminate >96% of genuine bird checklist data. Instead, Phase 3 will filter by eBird observation protocol (`traveling` distance $< 3\text{ km}$, `stationary`, and `all_species_reported = 1`).
3. **Temporal Surge**: Over 90% of records date from **2014 to 2024**. Raw record counts reflect observer effort and smartphone adoption rather than true biological population size.
4. **Status**: **`PARTIALLY VERIFIED`**. Validated for species distribution and detection/non-detection occupancy modeling; invalidated for naive longitudinal raw abundance counts.

---

## 5. GloBI Ecological Interaction Availability Audit

Using the Global Biotic Interactions (GloBI) REST API (`https://api.globalbioticinteractions.org/interaction`), we investigated interaction availability for key species known to occur in the three regions (*Panthera tigris*, *Elephas maximus*, *Axis axis*, *Cuon alpinus*, *Corvus splendens*, *Acridotheres tristis*, *Apis cerana*, *Pteropus giganteus*):

| Metric / Dimension | Finding | Audit Assessment |
| :--- | :--- | :---: |
| **Species-Level Interaction Presence** | Abundant global records exist for all test species (>100 interactions per species for tiger, chital, honeybee, crow). | `VERIFIED` |
| **Interaction Types Available** | `eats`, `preysOn`, `eatenBy`, `pollinates`, `hasParasite`, `hasPathogen`, `interactsWith`. | `VERIFIED` |
| **Geographic Coordinates (`lat`/`lon`)** | **0% of species interaction records have field coordinates** (values are `None`). | `PARTIALLY VERIFIED` |
| **Temporal Stamping (`observation_date`)** | **0% of species interaction records have dates** (values are `None`). | `PARTIALLY VERIFIED` |
| **Study Traceability** | Citations link to published literature, IUCN assessments, and Web of Life interaction matrices. | `VERIFIED` |
| **Global vs. Regional Nature** | **GloBI represents global literature knowledge, not localized Southern Indian field observations.** | `PARTIALLY VERIFIED` |

### Critical Methodological Finding for Phase 4:
GloBI cannot be treated as a spatially explicit observation dataset. Instead, GloBI provides the **taxonomic prior graph** (which species *can* eat, pollinate, or parasitize which other species). 
- In our research pipeline, regional food webs will be constructed by taking the **intersection of GloBI interaction links with regional species occurrence lists confirmed via GBIF**.
- *Rule 1 Compliance*: We will NOT invent missing interaction links. Unobserved links remain unlinked (sparse adjacency matrix).

---

## 6. Access Readiness for VIIRS-DNB & ESA WorldCover

### 6.1 VIIRS-DNB (Nighttime Light / ALAN)
- **Official Endpoint**: Earth Observation Group (EOG), Payne Institute for Public Policy, Colorado School of Mines: `https://eogdata.mines.edu/products/vnl/`
- **Product Selected**: **Annual VIIRS Nighttime Lights (VNL) Version 2.2** (`vnl_v22`, 15 arc-seconds ~500m).
- **Temporal Span**: 2012 to 2024 (annual composites), with monthly cloud-free composites available for seasonal analysis.
- **Regional Tile**: **Tile 3 (00N to 75N, 060E to 120E)** covers the Indian subcontinent. Spatial bounding boxes will be clipped from this tile.
- **Access Protocol**: Requires free registered EOG user account (automated via Python `requests` with HTTP Basic Authentication or via Google Earth Engine collection `NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG`).
- **Quality Bands**: Radiance in calibrated physical units ($\text{nW}\cdot\text{cm}^{-2}\cdot\text{sr}^{-1}$) and `cf_cvg` (cloud-free coverages tally).
- **Status**: **`VERIFIED`**.

### 6.2 ESA WorldCover (10m Land Cover)
- **Official Endpoint**: Open AWS S3 bucket: `s3://esa-worldcover/` and HTTPS `https://esa-worldcover.s3.eu-central-1.amazonaws.com/`. No credentials or registration required.
- **Available Epochs**: 2020 (`v100`) and 2021 (`v200`).
- **Covering Tiles (Verified Live)**:
  - `ESA_WorldCover_10m_2020_v100_N12E075_Map.tif` (HTTP 200, 140.3 MB): Covers **Bengaluru** and **Mysuru**.
  - `ESA_WorldCover_10m_2020_v100_N09E075_Map.tif` (HTTP 200, 86.3 MB): Covers **Nilgiri–Bandipur**.
  - `ESA_WorldCover_10m_2021_v200_N12E075_Map.tif` (HTTP 200, 127.6 MB): Covers **Bengaluru** and **Mysuru**.
  - `ESA_WorldCover_10m_2021_v200_N09E075_Map.tif` (HTTP 200, 75.6 MB): Covers **Nilgiri–Bandipur**.
- **Python Download / Extraction**: Cloud-Optimized GeoTIFFs (COGs) allow windowed spatial subsetting via `rasterio` or GDAL `/vsicurl/` directly streaming only our 50 km × 50 km bounding boxes without downloading unnecessary areas.
- **Relevant Classification Bands**: Class 10 (Tree cover), 20 (Shrubland), 30 (Grassland), 40 (Cropland), 50 (Built-up), 80 (Permanent water bodies), 90 (Wetland).
- **Status**: **`VERIFIED`**.

---

## 7. Synthetic-Data Integrity Audit

In compliance with Rule 1 ("ABSOLUTELY NO SYNTHETIC DATA"), an exhaustive regex audit across all non-venv project files was conducted:
- **Result**: `0` synthetic records, `0` random distributions (`np.random`, `random`), `0` simulated observations, `0` artificial fill-ins.
- All numbers, coordinates, and cell metrics derive strictly from deterministic geodetic formulas (`pyproj` / WGS 84 ellipsoid) or genuine HTTP API responses from GBIF, iNaturalist, OpenStreetMap, and AWS S3.
- **Status**: **`VERIFIED`**.

---

## 8. Outstanding Limitations & Decisions for User Approval

1. **Four-Dataset Constraint**: The project scope is officially frozen to VIIRS-DNB, GBIF, GloBI, and ESA WorldCover. No other datasets will be collected in Phase 2.
2. **Nilgiri–Bandipur Study Window Alignment**:
   - Current window captures 74.6% of Bandipur+Mudumalai OSM polygon area and includes Masinagudi, Moyar gorge, and Gundlupet while excluding Ooty town.
   - User decision required: Keep current window (`[11.4286°N–11.8832°N, 76.3658°E–76.8270°E]`) or slide 15km West / 10km North to maximize protected forest.
3. **GBIF Coordinate Uncertainty Handling**:
   - Because `coordinateUncertaintyInMeters` is absent in >96% of eBird checklist records, Phase 3 will rely on checklist protocol metadata (effort distance and duration) rather than numerical uncertainty thresholds.
4. **GloBI Integration Strategy**:
   - GloBI links will serve as a species-level interaction prior graph, intersected with regional species presence, rather than a point-level spatial observation layer.

---

## 9. Final Milestone Certification

**Phase 1 Final Approval Audit: COMPLETE.**
All geographical boundaries, 5 km grids, quality baselines, and data access routes for the four core datasets are verified. Zero synthetic data exists in the project.

**Phase 2 will begin only upon explicit user approval.**

