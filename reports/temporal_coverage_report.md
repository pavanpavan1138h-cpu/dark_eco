# Dark Ecology Intelligence (DEI) — Temporal Coverage Report

---

## 1. Executive Summary

This report establishes the temporal architecture for the **Dark Ecology Intelligence (DEI)** project across the target window of **1992–2024 (33 years)**. 

A rigorous scientific examination reveals that **no single empirical ecological or remote sensing dataset spans all 33 years continuously at uniform spatial and radiometric resolution**. Rather, the available data divides into distinct temporal regimes characterized by sensor transitions, structural discontinuities, citizen science growth curves, and static trait baselines.

To resolve these realities without fabricating data or introducing sensor artifacts into machine learning models, we propose a **two-tiered temporal modeling architecture**:
- **Tier 1: Multi-Decadal Macro Baseline (1992–2024, Annual Epochs)**: Evaluates macro-scale urban expansion, nightlight growth trajectories, climate shifts, and decadal habitat fragmentation using cross-calibrated sensors.
- **Tier 2: High-Fidelity Modern Ecological Horizon (2014–2024, Monthly/Seasonal Horizons)**: Conducts fine-scale trophic network modeling, species occupancy analysis, and lighting intervention simulations using high-dynamic-range VIIRS/Black Marble radiometry and dense citizen science biodiversity checklists.

---

## 2. Dataset Family Temporal Profiles

| Dataset Family | Primary Datasets | Temporal Span | Native Granularity | Temporal Regularity |
| :--- | :--- | :--- | :--- | :--- |
| **Nighttime Lights (ALAN)** | DMSP-OLS (v4) | 1992 – 2013 | Annual | Regular composites (cloud-free) |
| | VIIRS-DNB (EOG / VNL) | 2012 – 2024 | Monthly / Annual | Regular composites |
| | NASA Black Marble (VNP46) | 2012 – 2024 | Daily / Monthly / Annual | Regular (BRDF/lunar corrected) |
| | Harmonized NTL (Chen / Li) | 1992 – 2021 | Annual | Regular cross-calibrated |
| **Biodiversity Occurrences** | GBIF (Global Aggregator) | 1900 – 2024 | Exact date/time | Highly irregular (extreme post-2012 spike) |
| | eBird Basic Dataset (EBD) | 2000 – 2024 | Observation date/time | Highly seasonal; dense post-2014 |
| | iNaturalist Research-Grade | 2010 – 2024 | Observation date/time | Irregular; dense post-2016 only |
| **Species Functional Traits** | EltonTraits, AVONET, PanTHERIA | Static (2009–2022) | Single contemporary synthesis | Non-temporal (taxonomic attributes) |
| **Ecological Interactions** | GloBI, Mangal, Field Studies | Static / Undated | Taxonomic / literature records | Non-temporal interaction graph |
| **Environmental & Land Cover** | ESA WorldCover 10m | 2020 & 2021 | Annual snapshots | Two discrete modern epochs |
| | Hansen Global Forest Change | 2000 – 2023 | Annual tree loss year | Regular annual loss tracking |
| | WorldPop Gridded Population | 2000 – 2020 | Annual | Regular annual modeled |
| | GHSL Built Surface / Pop | 1975, 1990, 2000, 2015, 2020 | Multi-year epochs | 5-year to 15-year intervals |
| | ERA5-Land Reanalysis | 1950 – 2024 | Hourly / Monthly | Uninterrupted regular time series |
| | Copernicus DEM GLO-30 | Static (2011–2015 base) | Single contemporary surface | Non-temporal surface topography |
| | OpenStreetMap Vectors | Current / 2008–2024 | Cumulative edit history | Dynamic snapshot |
| **Validation Baselines** | WII All India Tiger Surveys | 2006, 2010, 2014, 2018, 2022 | Quadrennial reports | 4-year national monitoring cycles |
| | Mudumalai 50-ha Plot (IISc) | 1988 – 2023 | 5-year census intervals | Decadal permanent forest censuses |

---

## 3. Sensor Transitions & Radiometric Discontinuities in ALAN

The primary challenge in 33-year nightlight modeling is the profound physical and radiometric shift between **DMSP-OLS** and **VIIRS-DNB**.

```
1992       1995       2000       2005       2010   2012   2015       2020       2024
|---------- DMSP-OLS (1 km, 6-bit DN 0-63, No Calibration) ----------|
                                                   |--- VIIRS-DNB (500m, Radiance nW/cm²·sr) ---|
                                                   |-- NASA Black Marble (VNP46A2/A3/A4) -------|
|----------------- Harmonized Cross-Calibrated Time Series (Chen et al. 2021) ----------------|
```

### 3.1 DMSP-OLS (1992–2013) Limitations
1. **Sensor Saturation**: DMSP-OLS uses a 6-bit digital number ($0 \le \text{DN} \le 63$). In bright urban cores like central Bengaluru (Majestic, MG Road), the photomultiplier tube (PMT) saturated at $\text{DN} = 63$ as early as the late 1990s. Consequently, internal urban densification between 2000 and 2012 appears artificially flat.
2. **Lack of On-board Calibration**: Sensor degradation and gain adjustments occurred over time across six different satellites ($F10, F12, F14, F15, F16, F18$). Uncalibrated raw values cannot be used directly as a quantitative time series without inter-satellite pseudo-invariant target calibration (e.g. Elvidge et al. 2014).
3. **Coarse Spatial Resolution & Blooming Effect**: The nominal 30 arc-second (~1 km) grid suffers from significant geometric blooming / light scattering, exaggerating the spatial footprint of lit roads and villages into adjacent forest edges by up to 2–3 km.
4. **Overpass Timing**: Flown on sun-synchronous orbits with equatorial crossing times around **20:30–21:30 local solar time** (early evening, peak residential and commercial lighting).

### 3.2 VIIRS-DNB / NASA Black Marble (2012–Present) Advancements & Disparities
1. **High Radiometric Precision**: 14-bit quantized radiance measured in calibrated physical units ($\text{nW}\cdot\text{cm}^{-2}\cdot\text{sr}^{-1}$) spanning over 7 orders of magnitude, with zero saturation in urban centers.
2. **Finer Spatial Resolution**: 15 arc-seconds (~500 m pixel size), capturing individual road corridors and resolving micro-lighting around ecotourism lodges in Bandipur-Mudumalai.
3. **NASA Black Marble (VNP46A2/A3) Atmospheric and Lunar Correction**: Corrects for lunar phase, atmospheric scattering, surface bidirectional reflectance (BRDF), and thermal variations, providing reliable surface radiance.
4. **Overpass Timing Discrepancy**: Suomi-NPP and NOAA-20 cross the equator at approximately **01:30 AM local solar time**. This late-night overpass captures municipal street lighting and all-night industrial facilities, but misses decorative commercial lighting extinguished after midnight. **DMSP-OLS (~21:00) and VIIRS-DNB (~01:30) observe different nocturnal human regimes.**

### 3.3 Harmonized Longitudinal Solution
To bridge this gap for multi-decadal analysis, the project incorporates the peer-reviewed **Harmonized Global Nighttime Light Dataset** (Chen et al. 2021, *Nature Scientific Data*; Li et al. 2020, *Earth System Science Data*). These datasets use sigmoid-based calibration and autoencoder architectures to cross-calibrate DMSP-OLS to simulated VIIRS-like continuous radiances from 1992 through 2021, providing a consistent time series.

---

## 4. Biodiversity Temporal Structure: Biases & Realities

A critical finding of Phase 1 is that **biodiversity occurrence records across Southern India DO NOT represent a continuous, uniform annual time series from 1992 to 2024**.

```
Annual Occurrence Volume (Southern India)
Volume
  ^                                                    * (2024)
  |                                                  *
  |                                                *
  |                                              *  (Citizen Science Era)
  |                                            *
  |                                      *    *
  |                                    *
  |                             *     * (eBird India launch ~2014)
  |----------------------------*--------------------------------->
 1992         1998          2004          2010    2014   2020    2024
 [--- Historical Baseline ---] [ Early Modern ] [ Dense Checklists ]
```

### 4.1 Temporal Eras in Regional Biodiversity Data
1. **The Historical Specimen Era (1992–2005)**:
   - Data in GBIF is restricted to institutional museum collections, university specimens, and published research expeditions.
   - Observations are sparse, spatially clustered around botanical gardens (Lalbagh, Cubbon Park), Bangalore University, or forest research stations in Mudumalai/Bandipur.
   - *Risk*: Treating specimen volume as an index of true species abundance is scientifically invalid due to extreme collection bias.
2. **The Early Digital Era (2006–2013)**:
   - Early eBird records, institutional checklists (WII, IISc), and introductory digital recording.
   - Modest annual observation numbers; high variance across years.
3. **The Citizen Science Era (2014–2024)**:
   - Massive inflection point. The organized rollout of **Bird Count India**, the Great Backyard Bird Count (GBBC India), and widespread smartphone adoption led to an exponential increase in bird observations.
   - Post-2016: **iNaturalist** research-grade observations expanded across non-avian taxa (moths, amphibians, reptiles, mammals).

### 4.2 Methodological Solution: Effort Standardization & Occupancy Modeling
Because raw record counts reflect observer effort rather than actual population density, our Phase 3 data pipeline will implement:
- **Complete Checklist Filtering (eBird)**: Utilizing only checklists where the observer explicitly confirmed `ALL SPECIES REPORTED = YES`.
- **Observer Effort Covariates**: Incorporating duration (minutes), distance traveled (km), and time of observation into hierarchical detection/non-detection occupancy models ($z_i \sim \text{Bernoulli}(\psi_i)$).
- **Target-Group Background Sampling**: For presence-only GBIF and iNaturalist data, selecting background/pseudo-absence points from observations of related taxa within the same spatial grid cells to account for spatial sampling bias.

---

## 5. Environmental Variables: Temporal Resolution & Gaps

### 5.1 Land Cover Discontinuities
- **ESA WorldCover (10m)**: Provides exceptional spatial granularity (10 meters) but is available only for **2020 and 2021**. It serves as the contemporary land cover baseline.
- **Global Human Settlement Layer (GHSL - JRC)**: Provides multi-decadal built surface area (`GHS-BUILT-S`) at discrete epochs (**1975, 1990, 2000, 2015, 2020, 2025**). Linear and cubic spline interpolation will be applied between epochs to derive annual built-up area fractions for each 5 km × 5 km cell.
- **Hansen Global Forest Change (2000–2023)**: Provides exact annual forest loss year for every 30 m pixel. Valid for assessing forest loss and canopy degradation over the last 24 years, but does not provide forest change prior to 2000.

### 5.2 Climate Covariates (ERA5-Land)
- **Continuous 1992–2024 Coverage**: ERA5-Land provides continuous, hourly and monthly climate data (2m temperature, rainfall, soil moisture, solar radiation) with complete temporal continuity across all 33 years.

---

## 6. Recommended Two-Tiered Modeling Architecture

To maintain complete scientific integrity while maximizing data value, the DEI analytical roadmap adopts a two-tiered strategy:

```
+-------------------------------------------------------------------------------+
|                       TWO-TIERED TEMPORAL ARCHITECTURE                        |
|                                                                               |
|  [TIER 1] Multi-Decadal Macro Baseline (1992 - 2024)                          |
|  • Scope: 33 Annual Time Steps                                                |
|  • Nightlights: Harmonized DMSP-VIIRS Time Series (1 km)                      |
|  • Environment: GHSL Built Surface Epochs + ERA5-Land Climate                 |
|  • Ecology: Decadal species persistence, museum presence, protected trends   |
|  • Objective: Decadal macro-expansion and long-term land-system dynamics     |
|                                                                               |
|  [TIER 2] High-Fidelity Modern Ecological Horizon (2014 - 2024)               |
|  • Scope: 10 Years, Monthly / Seasonal Time Steps                             |
|  • Nightlights: VIIRS-DNB / NASA Black Marble BRDF Radiance (500 m)           |
|  • Environment: ESA WorldCover (10m) + Hansen Forest Loss (30m) + ERA5-Land   |
|  • Ecology: eBird Complete Checklists + iNaturalist Research-Grade + Traits  |
|  • Objective: Spatio-Temporal Graph Neural Networks, Trophic Interaction      |
|               Flows, and Lighting Optimization / Intervention Simulations     |
+-------------------------------------------------------------------------------+
```

This structure ensures that Phase 2 through Phase 5 avoid false assumptions while enabling valid multi-decadal and contemporary machine learning formulations.

