# Phase 1 Completion Report: Research Setup, Geographical Definition, and Dataset Source Inventory
**Dark Ecology Intelligence (DEI) — Artificial Neural Networks Problem-Based Learning (ANN PBL)**

---

## 1. Summary of Work Completed

In Phase 1 of the Dark Ecology Intelligence (DEI) project, we completed foundational research setup, geographical study-area boundaries, spatial-temporal frameworks, and a comprehensive inventory of 26 empirical remote sensing and ecological datasets.

Key milestones accomplished:
1. **Workspace Architecture**: Constructed the project directory hierarchy exclusively within `dark_eco/`, ensuring strict separation of raw data, processed arrays, metadata, GIS boundaries, modular phase scripts, and reports.
2. **Geographical Boundary Definition**: Mathematically established the three study-area windows (Bengaluru, Mysuru, Nilgiri–Bandipur), resolving specific scientific and ecological justifications for each, including explicitly bounding the Bandipur–Mudumalai corridor landscape separate from the wider Nilgiri Biosphere Reserve.
3. **Common Spatial Framework**: Implemented a mathematically rigorous 5 km × 5 km regular grid (100 cells per landscape = 300 total cells, covering 7,500 km²) projected in UTM Zone 43N (EPSG:32643) and generated GIS-compatible GeoJSON vector assets in WGS 84 (EPSG:4326).
4. **Temporal Scope Investigation**: Evaluated dataset availability across the 1992–2024 target window, identifying critical sensor transitions (DMSP-OLS saturation and calibration shifts to VIIRS-DNB) and biodiversity observer effort biases (museum records vs. post-2014 citizen science surge), establishing a two-tiered modeling architecture.
5. **Dataset Inventory & Regional Availability**: Cataloged 26 datasets across six categories (Nighttime Lights, Biodiversity Occurrences, Ecological Interactions, Species Traits, Environmental Covariates, and Independent Validation), producing detailed CSVs and comparative matrices.
6. **Execution Scripts**: Authored and verified standalone, reproducible Python scripts (`generate_boundaries_and_grids.py` and `generate_inventory_and_matrix.py`) requiring only standard libraries.

---

## 2. Geographical Boundary Recommendations

| Metric | Landscape 1: Bengaluru | Landscape 2: Mysuru | Landscape 3: Nilgiri–Bandipur |
| :--- | :--- | :--- | :--- |
| **Landscape Typology** | Highly Urbanised & Peri-Urban Gradient | Peri-Urban & Transitional Agricultural Matrix | Protected Forest & Transboundary Wildlife Corridor |
| **Centroid (WGS84)** | 12.9716° N, 77.5946° E (Vidhana Soudha) | 12.3051° N, 76.6551° E (Mysuru Palace) | 11.6600° N, 76.6000° E (Moyar Gorge / Interstate Border) |
| **Latitude Extent** | 12.7396° N – 13.1959° N (~50.5 km) | 12.0790° N – 12.5338° N (~50.3 km) | 11.4286° N – 11.8832° N (~50.3 km) |
| **Longitude Extent** | 77.3577° E – 77.8229° E (~50.4 km) | 76.4242° E – 76.8866° E (~50.2 km) | 76.3658° E – 76.8270° E (~50.2 km) |
| **UTM Zone 43N Bounds** | Easting: 756,000–806,000 m; Northing: 1,410,000–1,460,000 m | Easting: 655,000–705,000 m; Northing: 1,336,000–1,386,000 m | Easting: 649,000–699,000 m; Northing: 1,264,000–1,314,000 m |
| **Total Window Area** | 2,500 km² (10 × 10 cells) | 2,500 km² (10 × 10 cells) | 2,500 km² (10 × 10 cells) |
| **Key Anchor Features** | BBMP municipal core, Electronic City, Whitefield, Hesaraghatta lake, northern Bannerghatta NP buffer. | Mysuru City Corporation, Chamundi Hill Reserve Forest, Srirangapatna, Ranganathittu, Cauvery/Kabini basins. | Bandipur National Park (WDPA 862), Mudumalai Tiger Reserve (WDPA 863), Sigur Elephant Corridor, NH 766 & NH 181. |

### Scientific Justification: Nilgiri–Bandipur Landscape Delineation
Per instructions, the Nilgiri–Bandipur study area is explicitly defined as the **Bandipur–Mudumalai Transboundary Tiger Landscape and Moyar/Sigur Corridor**, rather than the entire Nilgiri Biosphere Reserve (NBR). The NBR spans over 5,520 km² and contains disparate montane shola and wet evergreen biomes. Our 50 km × 50 km study window captures the contiguous dry and moist deciduous forest tract bridging Karnataka and Tamil Nadu, encompassing the core wildlife corridor connecting the Western and Eastern Ghats while capturing critical nocturnal lighting frontiers (highways NH-766/181 and ecotourism lodge clusters in Masinagudi/Bokkapuram).

---

## 3. Spatial-Grid Recommendation

- **Grid Resolution**: Standardized **5.0 km × 5.0 km regular square cells** ($25.0\text{ km}^2$ per cell).
- **Coordinate Reference System**:
  - Projected Metric CRS: **WGS 84 / UTM Zone 43N (EPSG:32643)** for exact metric spacing and Euclidean calculations.
  - Storage/Interoperability CRS: **WGS 84 (EPSG:4326)** for GeoJSON and raster exports.
- **Sample Design**: 10 rows × 10 columns per region = 100 cells per region; **300 cells total across the study system (7,500 km² total coverage)**.
- **Handling Water Bodies & Missing Coverage**:
  - Grid cells overlapping water bodies (KRS, Kabini, Bellandur lake) will not be discarded; the `land_area_fraction` derived from ESA WorldCover (Class 80) will be attached as a structural covariate.
  - Monsoon cloud masking in optical and nightlight imagery will be imputed using seasonal baseline spline interpolation rather than treated as dark cells.
  - Boundary padding and Queen/Rook contiguity will define spatial graph adjacency matrices for Graph Neural Network formulations.

---

## 4. Temporal Coverage Findings (1992–2024)

1. **ALAN Radiometer Shift**:
   - **DMSP-OLS (1992–2013)**: 6-bit uncalibrated digital numbers ($0 \le \text{DN} \le 63$), suffering from severe saturation in Bengaluru city center and spatial blooming (~1 km resolution). Equatorial overpass: ~21:00 local solar time.
   - **VIIRS-DNB / NASA Black Marble (2012–2024)**: 14-bit calibrated radiance ($\text{nW}\cdot\text{cm}^{-2}\cdot\text{sr}^{-1}$), 500 m resolution, no saturation, lunar/atmospheric corrections. Equatorial overpass: ~01:30 local solar time.
   - *Harmonized Solution*: Cross-calibrated DMSP-VIIRS datasets (Chen et al. 2021) will be used for continuous 1992–2021 macro-trend analysis.
2. **Biodiversity Temporal Heterogeneity**:
   - Pre-2005 data is sparse and restricted to museum specimen collections.
   - A dramatic citizen science surge occurs post-2014 (eBird India launch) and post-2016 (iNaturalist).
   - Biodiversity observations cannot be treated as a continuous annual abundance time series. We must apply **detection/non-detection occupancy modeling** on eBird complete checklists (`ALL SPECIES REPORTED = YES`) and **target-group background sampling** for presence-only data.
3. **Two-Tiered Architecture**:
   - **Tier 1 (Macro Historical, 1992–2024, Annual)**: Evaluates macro-scale urban expansion, harmonized nightlight growth, climate shifts (ERA5-Land), and decadal settlement patterns (GHSL).
   - **Tier 2 (Modern Ecological, 2014–2024, Monthly/Seasonal)**: High-resolution trophic network modeling and intervention simulations using VIIRS-DNB/Black Marble and dense citizen science biodiversity data.

---

## 5. Complete Dataset Source Inventory

The table below summarizes the 26 investigated datasets cataloged in [`dataset_inventory.csv`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/dataset_inventory.csv):

| # | Category | Dataset Name | Temporal Span | Spatial Res. | Access Mode | Official Source / URL |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | A. ALAN | DMSP-OLS Nighttime Lights v4 | 1992–2013 | ~1 km | Open (GEE/NOAA) | https://www.ngdc.noaa.gov/eog/dmsp/ |
| 2 | A. ALAN | VIIRS-DNB Monthly/Annual (EOG) | 2012–2024 | ~500 m | Open (EOG/GEE) | https://eogdata.mines.edu/products/vnl/ |
| 3 | A. ALAN | NASA Black Marble (VNP46A2-A4) | 2012–2024 | ~500 m | Free Auth Token | https://blackmarble.gsfc.nasa.gov/ |
| 4 | A. ALAN | Harmonized DMSP-VIIRS (Chen/Li) | 1992–2021 | ~1 km | Open (Zenodo/Figshare)| https://doi.org/10.1038/s41597-020-0510-y |
| 5 | B. Biodiversity | GBIF Biodiversity Occurrences | 1900–2024 | Point | Open (API/DOI) | https://www.gbif.org/ |
| 6 | B. Biodiversity | eBird Basic Dataset (EBD) | 2000–2024 | Point/Transect| Academic Request | https://ebird.org/science/download-ebird-data |
| 7 | B. Biodiversity | iNaturalist Research-Grade | 2010–2024 | Point | Open (API/DwC-A) | https://www.inaturalist.org/ |
| 8 | C. Food Webs | Global Biotic Interactions (GloBI) | Undated/Static| Network Graph | Open (REST API) | https://www.globalbioticinteractions.org/ |
| 9 | C. Food Webs | Mangal Ecological Networks | Static Archive| Network Graph | Open (REST API) | https://mangal.io/ |
| 10 | C. Food Webs | Published Indian Interaction Studies | 1988–2023 | Study Plot | Manual Curation | ATREE, IISc CES, WII Literature |
| 11 | D. Traits | EltonTraits 1.0 (Birds & Mammals) | Static (2014) | Species Table | Open (ESA Archives) | https://doi.org/10.1890/13-1917.1 |
| 12 | D. Traits | AVONET Avian Morphology/Traits | Static (2022) | Species Table | Open (Figshare) | https://doi.org/10.1111/ele.13898 |
| 13 | D. Traits | PanTHERIA Mammal Traits | Static (2009) | Species Table | Open (ESA Archives) | https://doi.org/10.1890/08-1494.1 |
| 14 | D. Traits | AmphiBIO Amphibian Traits | Static (2017) | Species Table | Open (Figshare) | https://doi.org/10.1038/sdata.2017.123 |
| 15 | E. Environment | ESA WorldCover 10m Land Cover | 2020 & 2021 | 10 meters | Open (COG/GEE) | https://esa-worldcover.org/ |
| 16 | E. Environment | Hansen Global Forest Change | 2000–2023 | 30 meters | Open (GEE/HTTP) | https://glad.earthengine.app/ |
| 17 | E. Environment | WorldPop Population Density | 2000–2020 | ~100 meters | Open (Direct/GEE) | https://www.worldpop.org/ |
| 18 | E. Environment | GHSL Built Surface & Settlement | 1975–2025 | 100m / 1km | Open (JRC Portal) | https://ghsl.jrc.ec.europa.eu/ |
| 19 | E. Environment | ERA5-Land Surface Climate | 1950–2024 | ~9 km | Free CDS API Key | https://cds.climate.copernicus.eu/ |
| 20 | E. Environment | Copernicus DEM (GLO-30) | Static (2015) | 30 meters | Open (AWS S3) | https://registry.opendata.aws/copernicus-dem/ |
| 21 | E. Environment | OpenStreetMap Infrastructure | Current/Oshdb | Vector (Meters)| Open (Geofabrik) | https://download.geofabrik.de/ |
| 22 | E. Environment | WDPA Protected Area Boundaries | Current Legal | Vector Polygon | Open (Protected Planet)| https://www.protectedplanet.net/ |
| 23 | F. Validation | BioTIME Biodiversity Time Series | Multidecadal | Plot GPS | Open (Direct) | https://biotime.st-andrews.ac.uk/ |
| 24 | F. Validation | PREDICTS Land-Use Responses | 1984–2016 | Site GPS | Open (NHM London) | https://data.nhm.ac.uk/dataset/predicts-database |
| 25 | F. Validation | WII All India Tiger Reports | 2006–2022 | 2km Grid/Beat | Reports Open | https://wii.gov.in/ |
| 26 | F. Validation | Mudumalai 50-ha Plot (ForestGEO) | 1988–2023 | 20m Subquadrat | Formal Request | https://forestgeo.si.edu/sites/asia/mudumalai |

---

## 6. Regional Availability Matrix

The matrix below reflects empirical data availability across the three landscapes from [`regional_availability_matrix.csv`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/regional_availability_matrix.csv):

| Dataset Name | Bengaluru Availability | Mysuru Availability | Nilgiri–Bandipur Availability | Collection Difficulty | Important Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DMSP-OLS NTL** | Confirmed available | Confirmed available | Confirmed available | Low | Saturation in Bengaluru core (DN=63); blooming effect into forest fringes. |
| **VIIRS-DNB Monthly** | Confirmed available | Confirmed available | Confirmed available | Low | Monsoon cloud cover voids (July–September); post-2012 only. |
| **NASA Black Marble** | Confirmed available | Confirmed available | Confirmed available | Low–Moderate | Requires Earthdata token; massive file volumes for daily data. |
| **Harmonized NTL** | Confirmed available | Confirmed available | Confirmed available | Low | 1 km resolution; smoothing in calibration model; ends in 2021. |
| **GBIF Occurrences** | Confirmed available | Confirmed available | Confirmed available | Low | Extreme observer bias toward roads and parks; sparse pre-2010. |
| **eBird Basic Dataset**| Confirmed available | Confirmed available | Confirmed available | Moderate | Requires academic request; bird-specific; post-2014 density. |
| **iNaturalist** | Confirmed available | Confirmed available | Limited coverage | Low | Low coverage inside Bandipur core due to camera/safari restrictions; post-2016. |
| **GloBI Interactions** | Likely available | Likely available | Likely available | Low | Non-spatial global literature graph; requires taxonomic name matching. |
| **Mangal Networks** | Limited coverage | Limited coverage | Likely available | Low | Very few Indian urban food webs archived; forest webs applicable to Nilgiris. |
| **Published Indian Studies**| Confirmed available | Limited coverage | Confirmed available | High | Manual literature transcription required from institutional papers. |
| **EltonTraits 1.0** | Confirmed available | Confirmed available | Confirmed available | Low | Static species-level traits; assumes fixed nocturnal behavior. |
| **AVONET Traits** | Confirmed available | Confirmed available | Confirmed available | Low | Bird-specific; static morphology (hand-wing index, beak morphology). |
| **PanTHERIA Traits** | Confirmed available | Confirmed available | Confirmed available | Low | Mammal-specific; some small mammal trait gaps require phylogenetic imputation. |
| **AmphiBIO Traits** | Confirmed available | Confirmed available | Confirmed available | Low | Amphibian-specific; static traits. |
| **ESA WorldCover 10m** | Confirmed available | Confirmed available | Confirmed available | Low | Available for 2020 and 2021 only; no historical depth. |
| **Hansen Forest Change**| Confirmed available | Confirmed available | Confirmed available | Low | Starts 2000; urban trees often missed; cumulative forest gain only. |
| **WorldPop Density** | Confirmed available | Confirmed available | Confirmed available | Low | Modelled census disaggregation; overestimates in core forest enclaves. |
| **GHSL Built-Up** | Confirmed available | Confirmed available | Confirmed available | Low | 5-year/multi-year epochs; coarse resolution in 1975/1990 epochs. |
| **ERA5-Land Climate** | Confirmed available | Confirmed available | Confirmed available | Moderate | ~9 km resolution requires spatial interpolation over Nilgiri escarpment. |
| **Copernicus DEM** | Confirmed available | Confirmed available | Confirmed available | Low | Digital Surface Model (includes canopy/buildings); static. |
| **OpenStreetMap** | Confirmed available | Confirmed available | Confirmed available | Low–Moderate | `lit=*` tag is incomplete outside municipal urban centers. |
| **WDPA Boundaries** | Confirmed available | Confirmed available | Confirmed available | Low | Legal gazetted boundaries only; misses informal corridor linkages. |
| **BioTIME Database** | Unavailable | Unavailable | Likely available | Low | No plots in Bengaluru or Mysuru urban limits; Western Ghats plots adjacent. |
| **PREDICTS Database** | Limited coverage | Limited coverage | Confirmed available | Low | Snapshot studies across land-use gradients; not a continuous time series. |
| **WII Tiger Surveys** | Unavailable | Unavailable | Confirmed available | Moderate–High | Report summaries available; raw camera-trap coordinates legally restricted. |
| **Mudumalai 50-ha Plot**| Unavailable | Unavailable | Confirmed available | High | Localized to Mudumalai dry deciduous tract; woody vegetation only. |

---

## 7. Access Requirements and Known Obstacles

### 7.1 Authentication & Data Access Requirements
1. **NASA Earthdata Login**: Required for NASA Black Marble (VNP46A2/A3/A4) via LAADS DAAC. Requires generating a personal bearer token.
2. **eBird Academic Data Access**: Downloading the eBird Basic Dataset (EBD) for Karnataka and Tamil Nadu requires a formal academic access request form to the Cornell Lab of Ornithology (approval turnaround: 24–48 hours).
3. **Copernicus Climate Data Store (CDS)**: Programmatic retrieval of ERA5-Land requires creating a CDS user account, accepting data terms, and configuring `~/.cdsapirc` with the CDS API key.
4. **Earth Observation Group (EOG)**: Downloading raw VIIRS-DNB monthly composites directly from the Payne Institute requires a free registered user login.
5. **GBIF DOI Registration**: GBIF requires an active user account to launch bounding-polygon occurrence downloads that generate a permanent, citable digital object identifier (DOI).

### 7.2 Known Obstacles & Mitigations
- **Monsoon Cloud Masking**: During June–September, cloud cover obstructs optical and nighttime radiance sensors. *Mitigation*: Use cloud-free coverage counts (`cf_cvg`) to weight data and impute persistent missing values using harmonic seasonal interpolation.
- **DMSP Sensor Saturation**: Digital numbers cap at 63 in urban Bengaluru. *Mitigation*: Incorporate the cross-calibrated Harmonized Nighttime Light series (Chen et al. 2021) and calibrate against built surface area (`GHS-BUILT-S`).
- **Legal Restrictions on Raw Wildlife Microdata**: Raw individual camera-trap photo records from the National Tiger Conservation Authority (NTCA) are classified. *Mitigation*: Use open quadrennial report-level density estimates and peer-reviewed published studies.

---

## 8. Recommended Collection Order for Phases 2–5

```
+-------------------------------------------------------------------------------+
|                       RECOMMENDED DATA COLLECTION PIPELINE                     |
|                                                                               |
|  [PHASE 2: NIGHTTIME LIGHTS]                                                  |
|  Step 1: Download Harmonized 1992-2021 DMSP-VIIRS dataset (Zenodo/Figshare)   |
|  Step 2: Pull VIIRS-DNB annual/monthly composites (2012-2024 via GEE/EOG)     |
|  Step 3: Extract NASA Black Marble monthly VNP46A3 for high-precision modern  |
|                                                                               |
|  [PHASE 3: BIODIVERSITY OCCURRENCES]                                          |
|  Step 1: Submit eBird Academic Data Request immediately for Southern India    |
|  Step 2: Query GBIF REST API / download polygon extracts for 3 study windows   |
|  Step 3: Pull research-grade iNaturalist observations (moths, amphibians)     |
|  Step 4: Standardize taxonomy using Catalogue of Life / GBIF backbone         |
|                                                                               |
|  [PHASE 4: FOOD WEBS & SPECIES TRAITS]                                        |
|  Step 1: Download global trait databases (EltonTraits, AVONET, PanTHERIA)     |
|  Step 2: Join nocturnal/diurnal activity & trophic traits to species lists    |
|  Step 3: Query GloBI interaction API for observed species pairs               |
|  Step 4: Construct initial regional food web graph adjacency matrices         |
|                                                                               |
|  [PHASE 5: ENVIRONMENTAL COVARIATES]                                          |
|  Step 1: Clip Copernicus DEM (GLO-30) and compute elevation, slope, aspect   |
|  Step 2: Extract ESA WorldCover (10m) land-use class fractions per cell       |
|  Step 3: Extract Hansen Global Forest Change annual tree loss (2000-2023)     |
|  Step 4: Aggregate WorldPop density and GHSL built-up surface per cell        |
|  Step 5: Pull ERA5-Land monthly temperature, precipitation, solar radiation   |
+-------------------------------------------------------------------------------+
```

---

## 9. Unresolved Questions and Risks

1. **Overpass Timing Mismatch with Faunal Activity**:
   - VIIRS-DNB observes the Earth at ~01:30 AM, whereas peak crepuscular and early-nocturnal wildlife activity (foraging, bird chorus disruption, insect attraction) occurs between 19:00 and 22:00. This temporal offset may underestimate exposure to commercial and sports lighting that shuts off by midnight.
2. **Species Detection Bias along Protected Area Safari Routes**:
   - In Bandipur and Mudumalai, tourist sightings and eBird checklists are strictly restricted to designated safari routes and public highways. Interior wilderness areas may be underrepresented in citizen science records, necessitating distance-from-road bias weighting in Phase 3.
3. **Taxonomic Discrepancies Across Trait Databases**:
   - Taxonomic synonyms differ between eBird (Clements checklist), GBIF, and older trait syntheses (EltonTraits). A dedicated taxonomic crosswalk script will be required during Phase 4.

---

## 10. List of Files Created

The following 18 files and directories have been created inside the project workspace:

### Documentation and Reports
1. [`dark_eco/README.md`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/README.md): Project architecture and execution manual.
2. [`dark_eco/chat_history.txt`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/chat_history.txt): Persistent conversation log.
3. [`dark_eco/reports/geographical_framework.md`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/reports/geographical_framework.md): Detailed spatial framework and boundary justification report.
4. [`dark_eco/reports/temporal_coverage_report.md`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/reports/temporal_coverage_report.md): Sensor transitions and temporal architecture report.
5. [`dark_eco/reports/phase_reports/phase_1_completion_report.md`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/reports/phase_reports/phase_1_completion_report.md): This Phase 1 completion milestone report.

### Data Inventory and Availability Matrices
6. [`dark_eco/dataset_inventory.csv`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/dataset_inventory.csv) (mirrored in `dark_eco/reports/dataset_inventory/`)
7. [`dark_eco/regional_availability_matrix.csv`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/regional_availability_matrix.csv) (mirrored in `dark_eco/reports/dataset_inventory/`)

### Boundary and Grid GeoJSON Assets
8. [`dark_eco/geographical_boundaries/study_areas_summary.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/study_areas_summary.geojson)
9. [`dark_eco/geographical_boundaries/bengaluru_study_area.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/bengaluru_study_area.geojson)
10. [`dark_eco/geographical_boundaries/mysuru_study_area.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/mysuru_study_area.geojson)
11. [`dark_eco/geographical_boundaries/nilgiri_bandipur_study_area.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/nilgiri_bandipur_study_area.geojson)
12. [`dark_eco/geographical_boundaries/bengaluru_5km_grid.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/bengaluru_5km_grid.geojson)
13. [`dark_eco/geographical_boundaries/mysuru_5km_grid.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/mysuru_5km_grid.geojson)
14. [`dark_eco/geographical_boundaries/nilgiri_bandipur_5km_grid.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/nilgiri_bandipur_5km_grid.geojson)
15. [`dark_eco/geographical_boundaries/all_regions_5km_grid.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/all_regions_5km_grid.geojson)

### Phase 1 Python Generation Scripts
16. [`dark_eco/scripts/phase_1_setup/generate_boundaries_and_grids.py`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/scripts/phase_1_setup/generate_boundaries_and_grids.py)
17. [`dark_eco/scripts/phase_1_setup/generate_inventory_and_matrix.py`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/scripts/phase_1_setup/generate_inventory_and_matrix.py)

---

## 11. Milestone Status

**Phase 1 Status: COMPLETE.** 

All project structure setup, boundary delineations, grid generation, temporal coverage investigations, dataset source inventories, and regional availability matrices are established and verified. No datasets have been downloaded, and no machine learning models have been initiated. We await user authorization before initiating Phase 2.

