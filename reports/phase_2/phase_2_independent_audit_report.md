# Dark Ecology Intelligence (DEI) — Phase 2: Nighttime Lights
# FINAL INDEPENDENT AUDIT REPORT OF PHASE 2 VIIRS RESULTS

**Project**: Dark Ecology Intelligence (DEI) — Artificial Neural Networks Problem-Based Learning (ANN PBL)  
**Audit Date**: November 2026  
**Auditor Role**: Scientific Research Data Engineer & Independent Quality Auditor  
**Audit Target**: Complete Phase 2 Deliverables (25 Granules, 150 GeoTIFFs, 2 Gridded Tables, 6 Figures, 7 Notebooks, 5 Reports)  
**Project Root**: `dark_eco/`  
**Governing Rule**: Strict Evidence-Based Assessment | Zero Synthetic Data | No File Deletion | No Remote Git Push  

---

## Executive Summary of Audit Findings

An exhaustive, independent verification was performed on all Phase 2 code, data matrices, checksums, notebooks, figures, and spatial aggregation files. Every empirical number reported herein was recomputed directly from the underlying physical files.

| Audit Section | Evaluated Deliverable | Audit Status | Key Finding / Summary |
| :--- | :--- | :---: | :--- |
| **1. Raw Archive Verification** | 25 NASA Black Marble HDF5 Granules | **PASS** | Exactly 13 annual (2012–2024) and 12 monthly (2024) granules present on disk for Tile `h25v07`. All 25 open cleanly in `h5py`. |
| **2. Granule Integrity & Hashes** | SHA-256 Hashes & CMR Sizes | **PASS WITH CAVEATS** | All local file sizes match NASA CMR byte sizes within 0.01 MB. SHA-256 hashes independently recalculated; distinguished from source-side API hashes. |
| **3. HDF5 Metadata Audit** | Layer Dtypes, Offsets, Scales, Units | **PASS** | Exact dimensions `(2400, 2400)`, `float32`, units `nWatts/(cm^2 sr)`, scale 1.0, offset 0.0, fill `-999.9`. Exact coordinate arrays verified. |
| **4. QA & `_Num` Verification** | QA Flag Meanings & Obs Definition | **PASS WITH CAVEATS** | QA flags `0, 1, 2, 255` confirmed from metadata. Clarified that `_Num` is the count of Near-Nadir observations used in the composite, not total clear-sky satellite passes. |
| **5. Spatial Processing Audit** | GeoJSON Cropping, Alignment & Proj | **PASS** | Exact polygon-based slicing confirmed. Option A strictly retained. Reprojection to UTM 43N (500m) preserves radiometry with >99.75% fidelity. |
| **6. Annual Statistics Reproduction** | 13-Year Decadal Regional Means | **PASS** | Decadal increase confirmed: Bengaluru (19.09 to 26.79 nW), Mysuru (2.11 to 3.61 nW), Nilgiri–Bandipur (0.17 to 0.29 nW). |
| **7. Monthly Statistics Reproduction**| 12-Month Seasonal Cloud Dynamics | **PASS** | Pre-monsoon dry season (Jan–Apr) achieves 98–100% valid coverage. Southwest Monsoon (Jul) suffers severe cloud attenuation (0% in BLR, 4.8% in NIL). |
| **8. Grid-Level Validation** | 300 Grid Cells & Specific Claims | **PASS WITH CAVEATS** | Sarjapur (+275%), Whitefield (+87.8%), and Electronic City (+85%) confirmed. Yelahanka core was already developed in 2012 (-4.0% change). Nilgiri cells < 0.10 nW is **51%**, not 68%. |
| **9. Figure & Notebook Review** | 6 Figures & 7 Jupyter Notebooks | **PASS WITH CAVEATS** | All 7 notebooks execute with 0 errors. Identified filename/content mismatches: Figure 3 maps 2012–2024 (named `2023_2024`); Figure 4 graphs 12 months (named `march_vs_july`). |
| **10. Manifest & Reproducibility** | Manifest Indexing & Clean Workflow | **PASS** | All 177 research assets indexed in `viirs_dnb_manifest.csv` with zero missing files and zero byte discrepancies. Fully reproducible locally. |

---

## Section 1: Raw Archive Verification

### Audit Target:
Inspect all 25 NASA Black Marble Collection 2 HDF5 granules located in `dark_eco/data/raw/viirs_dnb/annual` and `dark_eco/data/raw/viirs_dnb/monthly`.

### Findings:
1. **Granule Completeness**:
   - **Annual Series (`VNP46A4`)**: Exactly 13 annual granules spanning calendar years 2012 through 2024 inclusive are present.
   - **Monthly Series (`VNP46A3`)**: Exactly 12 monthly granules spanning January through December 2024 inclusive are present.
   - Total raw files: **25 granules**.
2. **Collection Version & Spatial Tile**:
   - All 25 granules belong to NASA Collection 2 (`002` / `version_id = 2`).
   - All 25 granules correspond to Sinusoidal / Equirectangular Tile **`h25v07`** ($10.0^\circ–20.0^\circ\text{N}, 70.0^\circ–80.0^\circ\text{E}$).
3. **Internal Structure**:
   - Every file was opened using `h5py.File(path, 'r')`.
   - Every file contains the complete HDF-EOS group structure: `/HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data Fields/`.
   - Matrix dimensions are uniformly **$(2400, 2400)$** across all 25 granules.
4. **CMR Record Matching**:
   - Every granule filename exactly matches the `producer_granule_id` recorded in the NASA Common Metadata Repository (CMR) under collections `C3860065683-LAADS` (VNP46A4) and `C3860061042-LAADS` (VNP46A3).
   - No duplicate, corrupted, or misnamed files exist.

**Status**: **PASS**

---

## Section 2: Granule Integrity Results & SHA-256 Checksum Audit

### Audit Target:
Recalculate 256-bit SHA hashes for every raw file and compare against NASA CMR reported sizes and records.

### Empirical Evidence Table:

| Product | Period | Granule Identifier | Local File Size | NASA CMR Size | Size Match | Recalculated SHA-256 (Prefix...Suffix) |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| **VNP46A4** | 2012 | `VNP46A4.A2012001.h25v07.002.2025086171841.h5` | 102.96 MB | 102.96 MB | **Exact** | `5617a2c6582e15d2...d193d5f8` |
| **VNP46A4** | 2013 | `VNP46A4.A2013001.h25v07.002.2025087050240.h5` | 95.24 MB | 95.24 MB | **Exact** | `f7efb6d42a7f939a...06b12461` |
| **VNP46A4** | 2014 | `VNP46A4.A2014001.h25v07.002.2025091142056.h5` | 98.48 MB | 98.48 MB | **Exact** | `7b07be5e76e5ab68...82c89db1` |
| **VNP46A4** | 2015 | `VNP46A4.A2015001.h25v07.002.2025093112102.h5` | 101.05 MB | 101.05 MB | **Exact** | `090fa8690a1d4c3d...faad7649` |
| **VNP46A4** | 2016 | `VNP46A4.A2016001.h25v07.002.2025102110024.h5` | 98.19 MB | 98.19 MB | **Exact** | `a3cdef0a3bac041f...8233f545` |
| **VNP46A4** | 2017 | `VNP46A4.A2017001.h25v07.002.2025105150354.h5` | 97.01 MB | 97.01 MB | **Exact** | `e8a56618faef741a...bf5e1003` |
| **VNP46A4** | 2018 | `VNP46A4.A2018001.h25v07.002.2025114134507.h5` | 99.19 MB | 99.19 MB | **Exact** | `ec2414321c9fec91...f384931a` |
| **VNP46A4** | 2019 | `VNP46A4.A2019001.h25v07.002.2025134130254.h5` | 100.64 MB | 100.64 MB | **Exact** | `6c4c7ebb30443bac...3258a69e` |
| **VNP46A4** | 2020 | `VNP46A4.A2020001.h25v07.002.2025134021349.h5` | 98.36 MB | 98.36 MB | **Exact** | `50ccc31f4373c364...6b17042a` |
| **VNP46A4** | 2021 | `VNP46A4.A2021001.h25v07.002.2025149212913.h5` | 105.78 MB | 105.78 MB | **Exact** | `77aa7dd0b2604679...69018ee0` |
| **VNP46A4** | 2022 | `VNP46A4.A2022001.h25v07.002.2025156213204.h5` | 118.30 MB | 118.30 MB | **Exact** | `469d03f00cb916f8...d4576326` |
| **VNP46A4** | 2023 | `VNP46A4.A2023001.h25v07.002.2025162080718.h5` | 127.74 MB | 127.74 MB | **Exact** | `42a8aaa1a70e8b79...44e612778` |
| **VNP46A4** | 2024 | `VNP46A4.A2024001.h25v07.002.2025162125316.h5` | 124.04 MB | 124.04 MB | **Exact** | `2ed7d658fb146360...21d5864dd` |
| **VNP46A3** | 2024-01 | `VNP46A3.A2024001.h25v07.002.2025161152454.h5` | 109.02 MB | 109.02 MB | **Exact** | `aa85e3443d74f4ec...ca925e04` |
| **VNP46A3** | 2024-02 | `VNP46A3.A2024032.h25v07.002.2025161142752.h5` | 109.67 MB | 109.67 MB | **Exact** | `e2e0a0fcbaf1c513...6e16ba38` |
| **VNP46A3** | 2024-03 | `VNP46A3.A2024061.h25v07.002.2025119195201.h5` | 126.68 MB | 126.68 MB | **Exact** | `b34bc79053ae2acf...5ecb9829` |
| **VNP46A3** | 2024-04 | `VNP46A3.A2024092.h25v07.002.2025134112700.h5` | 125.19 MB | 125.19 MB | **Exact** | `416bd24bfa373674...327d7fc4` |
| **VNP46A3** | 2024-05 | `VNP46A3.A2024122.h25v07.002.2025139143057.h5` | 108.17 MB | 108.17 MB | **Exact** | `a6a65b4bd512f972...aa56396b` |
| **VNP46A3** | 2024-06 | `VNP46A3.A2024153.h25v07.002.2025139144711.h5` | 72.30 MB | 72.30 MB | **Exact** | `39a275a9b835e41a...e6b0ce3d` |
| **VNP46A3** | 2024-07 | `VNP46A3.A2024183.h25v07.002.2025139150250.h5` | 20.13 MB | 20.13 MB | **Exact** | `6290f3fa67e200d8...42119c8e` |
| **VNP46A3** | 2024-08 | `VNP46A3.A2024214.h25v07.002.2025119201857.h5` | 68.74 MB | 68.74 MB | **Exact** | `4d66f9a805c942c4...e69a03b5` |
| **VNP46A3** | 2024-09 | `VNP46A3.A2024245.h25v07.002.2025139152225.h5` | 96.12 MB | 96.12 MB | **Exact** | `55c3c65733d8ae3c...2db793bc` |
| **VNP46A3** | 2024-10 | `VNP46A3.A2024275.h25v07.002.2025119204315.h5` | 109.03 MB | 109.03 MB | **Exact** | `d3cca37e6d2d46e6...b8ad1607` |
| **VNP46A3** | 2024-11 | `VNP46A3.A2024306.h25v07.002.2025139154453.h5` | 108.69 MB | 108.69 MB | **Exact** | `95a44abed1033524...3a7ff303` |
| **VNP46A3** | 2024-12 | `VNP46A3.A2024336.h25v07.002.2025119210606.h5` | 111.39 MB | 111.39 MB | **Exact** | `862bc0294864bd1b...b6c93f0b` |

### Audit Qualification:
NASA CMR does not publish SHA-256 hashes in its standard JSON granule feeds (it reports exact byte sizes and Content-Length headers). Therefore, these SHA-256 hashes represent **independently recalculated local verification hashes**, verified byte-for-byte against the remote Content-Length reported by NASA LAADS DAAC.

**Status**: **PASS WITH CAVEATS** (File sizes match authoritative records exactly; checksums are locally computed reference baselines).

---

## Section 3: HDF5 Metadata and Geolocation Verification

### Audit Target:
Verify dataset attributes, data types, scaling, offsets, units, dimensions, and coordinate vectors across representative granules.

### Empirical Metadata Inspection:

```
Dataset: NearNadir_Composite_Snow_Free
  dtype: float32 | shape: (2400, 2400)
  units: nWatts/(cm^2 sr)
  scale_factor: 1.0 | offset: 0.0
  _FillValue: -999.9
  valid_range: >= 0.0

Dataset: NearNadir_Composite_Snow_Free_Quality
  dtype: uint8 | shape: (2400, 2400)
  units: flag, no units
  scale_factor: 1.0 | offset: 0.0
  _FillValue: 255
  valid_range: [0, 254]

Dataset: NearNadir_Composite_Snow_Free_Num
  dtype: uint16 | shape: (2400, 2400)
  units: number of observations
  scale_factor: 1.0 | offset: 0.0
  _FillValue: 65535
  valid_range: [0, 65534]

Dataset: Land_Water_Mask
  dtype: uint8 | shape: (2400, 2400)
  units: land water mask, no units
  _FillValue: 255
  classes: 0=Land & Desert, 1=Land no Desert, 2=Inland Water, 3=Sea Water, 5=Coastal
```

### Geolocation & Grid Step Verification:
- **Latitude Vector (`lat`)**: 2400 elements, monotonically decreasing from $20.0000^\circ\text{N}$ down to $10.0042^\circ\text{N}$. Step: $\Delta \text{lat} = 0.004166667^\circ$ ($15.0\text{ arc-seconds}$).
- **Longitude Vector (`lon`)**: 2400 elements, monotonically increasing from $70.0000^\circ\text{E}$ up to $79.9958^\circ\text{E}$. Step: $\Delta \text{lon} = 0.004166667^\circ$ ($15.0\text{ arc-seconds}$).
- **CRS**: Geographic equirectangular WGS84 coordinate reference system (`EPSG:4326`).

**Status**: **PASS**

---

## Section 4: QA Flag Definitions and the Exact Meaning of `_Num`

### Audit Target:
Investigate QA categories and specifically verify the definition and meaning of `_Num`.

### 1. Rigorous Definition of `_Num`:
- **Prior Potential Misstatement**: Casual terminology calling `_Num` the "total clear-sky overpasses of the satellite".
- **Official NASA Product Definition**:
  > *`long_name`: "Number of Observations of Temporal Radiance Composite Using Near Nadir Angle Observations (View Zenith Angle 0-20 degree) During Snow-free Period"*
- **Scientific Audit Finding**: `_Num` represents the **exact count of valid observations retained and integrated into that specific angular composite** (0°–20° zenith angle). It does **NOT** equal the total clear-sky overpasses of the VIIRS satellite, because:
  1. Overpasses where the satellite viewed the pixel at zenith angles $> 20^\circ$ are routed into the `OffNadir_Composite_Snow_Free` composite.
  2. Overpasses degraded by cloud edges or calibration flags are filtered out prior to compositing.
  3. Therefore, `_Num` measures **effective sample weight per pixel in the Near-Nadir composite**, not total satellite passes.

### 2. Quality Flag Categories (`NearNadir_Composite_Snow_Free_Quality`):
- `0` = **Good Quality**: Optimal cloud-free near-nadir observation.
- `1` = **Poor Quality**: Cloud fringe, high solar/lunar zenith, or degraded confidence.
- `2` = **Gap Filled**: BRDF model or temporal fallback replacement.
- `255` = **Fill Value**: Missing or obstructed by persistent cloud cover.

**Status**: **PASS WITH CAVEATS** (`_Num` definition formally clarified and qualified).

---

## Section 5: Independent Reproduction of Quality Statistics

### Audit Target:
Recalculate quality statistics directly from raw HDF5 arrays across all 25 granules.

### Full Tile `h25v07` ($5,760,000$ pixels) Reproduction Table:

| Product | Period | Good Q Pixels | Poor Q Pixels | Gap-Filled Pixels | Fill Pixels | Valid Pct (%) | Good Q Pct (%) | Mean `_Num` | Max `_Num` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **VNP46A4** | 2012 | 5,758,252 | 0 | 1,730 | 18 | **100.00%** | **99.97%** | 27.7 | 58 |
| **VNP46A4** | 2013 | 5,758,284 | 0 | 1,700 | 16 | **100.00%** | **99.97%** | 30.0 | 64 |
| **VNP46A4** | 2014 | 5,758,954 | 0 | 1,030 | 16 | **100.00%** | **99.98%** | 30.5 | 68 |
| **VNP46A4** | 2015 | 5,758,416 | 0 | 1,567 | 17 | **100.00%** | **99.97%** | 30.4 | 67 |
| **VNP46A4** | 2016 | 5,758,740 | 0 | 1,244 | 16 | **100.00%** | **99.98%** | 32.2 | 65 |
| **VNP46A4** | 2017 | 5,758,765 | 0 | 1,220 | 15 | **100.00%** | **99.98%** | 31.2 | 63 |
| **VNP46A4** | 2018 | 5,757,213 | 0 | 2,772 | 15 | **100.00%** | **99.95%** | 30.7 | 66 |
| **VNP46A4** | 2019 | 5,757,980 | 0 | 2,005 | 15 | **100.00%** | **99.96%** | 29.9 | 61 |
| **VNP46A4** | 2020 | 5,757,512 | 0 | 2,473 | 15 | **100.00%** | **99.96%** | 29.6 | 58 |
| **VNP46A4** | 2021 | 5,757,744 | 0 | 2,241 | 15 | **100.00%** | **99.96%** | 27.3 | 58 |
| **VNP46A4** | 2022 | 5,758,260 | 0 | 1,725 | 15 | **100.00%** | **99.97%** | 29.1 | 58 |
| **VNP46A4** | 2023 | 5,758,272 | 0 | 1,714 | 14 | **100.00%** | **99.97%** | 33.2 | 67 |
| **VNP46A4** | 2024 | 5,758,416 | 0 | 1,570 | 14 | **100.00%** | **99.97%** | 28.3 | 64 |
| **VNP46A3** | 2024-01 | 3,575,066 | 0 | 2,184,845 | 89 | **100.00%** | **62.07%** | 3.9 | 8 |
| **VNP46A3** | 2024-02 | 4,382,912 | 0 | 1,376,960 | 128 | **100.00%** | **76.09%** | 4.3 | 7 |
| **VNP46A3** | 2024-03 | 4,807,032 | 0 | 952,864 | 104 | **100.00%** | **83.46%** | 4.9 | 8 |
| **VNP46A3** | 2024-04 | 3,059,252 | 0 | 2,700,172 | 576 | **99.99%** | **53.11%** | 3.6 | 8 |
| **VNP46A3** | 2024-05 | 281,048 | 0 | 5,403,818 | 75,134 | **98.70%** | **4.88%** | 1.7 | 7 |
| **VNP46A3** | 2024-06 | 450 | 0 | 4,771,280 | 988,270 | **82.84%** | **0.01%** | 0.2 | 4 |
| **VNP46A3** | 2024-07 | 12 | 0 | 1,263,099 | 4,496,889 | **21.93%** | **0.00%** | 0.1 | 2 |
| **VNP46A3** | 2024-08 | 720 | 0 | 4,489,587 | 1,269,693 | **77.96%** | **0.01%** | 0.3 | 5 |
| **VNP46A3** | 2024-09 | 10,240 | 0 | 5,716,595 | 33,165 | **99.42%** | **0.18%** | 0.9 | 6 |
| **VNP46A3** | 2024-10 | 475,200 | 0 | 5,276,058 | 8,742 | **99.85%** | **8.25%** | 1.7 | 7 |
| **VNP46A3** | 2024-11 | 2,764,224 | 0 | 2,972,107 | 23,669 | **99.59%** | **47.99%** | 3.3 | 8 |
| **VNP46A3** | 2024-12 | 2,881,152 | 0 | 2,878,830 | 18 | **100.00%** | **50.02%** | 3.6 | 8 |

### Critical Identification of Weak Monthly Coverage:
- In **July 2024**, **78.07% of pixels across Tile `h25v07` are missing/fill** (4,496,889 pixels obstructed). In our Southern Karnataka study areas, July valid coverage is **0.0% in Bengaluru**, **18.2% in Mysuru**, and **4.8% in Nilgiri–Bandipur**.
- In **June, August, and September 2024**, while gap-filling restores numerical values across 78–99% of pixels, the **direct Good Quality (QF=0) percentage is $< 0.2\%$**, with mean observations used dropping below $0.5$ per pixel.
- **Consequence for Modeling**: Single-month monsoon composites must **not** be treated as directly observed nighttime light. Machine learning models must use annual baselines, or restrict seasonal analysis to the dry season (Jan–Apr) and post-monsoon (Nov–Dec).

**Status**: **PASS**

---

## Section 6: Spatial Processing Audit & Resampling Effects

### Audit Target:
Inspect GeoJSON study boundaries, grid files, exact polygon cropping, coordinate alignment, NoData preservation, and resampling fidelity.

### 1. Spatial Boundary Verification:
- All three original study windows (`study_areas_summary.geojson`) are retained.
- **Nilgiri–Bandipur Option A** (`[11.4286°N–11.8832°N, 76.3658°E–76.8270°E]`) is strictly preserved without boundary shifts.
- All 300 5 km grid cells (`all_regions_5km_grid.geojson`) are accounted for.

### 2. Resampling & Reprojection Fidelity (WGS84 vs UTM Zone 43N):
We evaluated whether bilinear resampling from native 15 arc-sec WGS84 to 500 m UTM Zone 43N introduces systematic radiance distortion across representative time periods:

| Period | Region | WGS84 Native Mean | UTM 43N Resampled Mean | Absolute Difference | Relative Difference |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Annual 2012** | **Bengaluru** | 18.646 nW | 18.661 nW | $+0.0145\text{ nW}$ | **+0.08%** |
| **Annual 2012** | **Mysuru** | 2.078 nW | 2.077 nW | $-0.0011\text{ nW}$ | **-0.05%** |
| **Annual 2012** | **Nilgiri–Bandipur**| 0.170 nW | 0.170 nW | $+0.0002\text{ nW}$ | **+0.13%** |
| **Annual 2024** | **Bengaluru** | 26.315 nW | 26.378 nW | $+0.0629\text{ nW}$ | **+0.24%** |
| **Annual 2024** | **Mysuru** | 3.561 nW | 3.558 nW | $-0.0023\text{ nW}$ | **-0.06%** |
| **Annual 2024** | **Nilgiri–Bandipur**| 0.289 nW | 0.290 nW | $+0.0007\text{ nW}$ | **+0.23%** |

### Audit Finding:
The difference between native unprojected WGS84 crops and UTM Zone 43N 500 m rasters is **$< 0.25\%$** across all regions. Radiometric scale, contrast, and NoData markers (`-999.9`) are preserved with $>99.75\%$ fidelity.

**Status**: **PASS**

---

## Section 7: Independent Reproduction of Annual & Monthly Statistics

### Audit Target:
Independently reproduce regional annual means (2012–2024) and monthly 2024 summaries from the 5 km gridded metrics tables.

### 13-Year Decadal Regional Mean Trajectory Table:

$$\text{Regional Mean Radiance } (\text{nW}\cdot\text{cm}^{-2}\cdot\text{sr}^{-1})$$

| Year | Bengaluru (Urban) | Mysuru (Transitional) | Nilgiri–Bandipur (Forest Option A) |
| :---: | :---: | :---: | :---: |
| **2012** | 19.09 nW | 2.11 nW | 0.17 nW |
| **2013** | 19.12 nW | 1.97 nW | 0.09 nW |
| **2014** | 20.46 nW | 2.27 nW | 0.13 nW |
| **2015** | 21.06 nW | 2.45 nW | 0.14 nW |
| **2016** | 21.28 nW | 2.50 nW | 0.12 nW |
| **2017** | 21.32 nW | 2.44 nW | 0.10 nW |
| **2018** | 21.84 nW | 2.65 nW | 0.11 nW |
| **2019** | 21.90 nW | 2.61 nW | 0.12 nW |
| **2020** | 21.23 nW | 2.54 nW | 0.11 nW |
| **2021** | 22.67 nW | 2.92 nW | 0.12 nW |
| **2022** | 23.82 nW | 2.93 nW | 0.20 nW |
| **2023** | 26.20 nW | 3.27 nW | 0.25 nW |
| **2024** | 26.79 nW | 3.61 nW | 0.29 nW |
| **Decadal $\Delta$ (2024–2012)** | **+7.70 nW** | **+1.50 nW** | **+0.12 nW** |
| **Relative Growth (%)** | **+40.3%** | **+71.1%** | **+70.6%** |

*(Note: In earlier summary text, 2012 was approximated using unweighted raster crop means as 18.01 nW yielding +48.7% growth; when calculated strictly on the 100 5 km grid cell centroids, 2012 mean is 19.09 nW yielding +40.3% growth).*

**Status**: **PASS**

---

## Section 8: Grid-Level Validation & Audit of Specific Claims

### 1. Audit of the Nilgiri–Bandipur $< 0.10\text{ nW}$ Cell Statistic:
- **Prior Claim in Report Text**: *"68% of the 5 km grid cells in Nilgiri–Bandipur have an annual mean radiance below 0.10 nW/cm²/sr"*.
- **Empirical Recalculation on Actual 100 Cells**:
  - In 2024: Exactly **51 cells (51.0%)** have mean radiance $< 0.10\text{ nW}$.
  - In 2012: Exactly **56 cells (56.0%)** have mean radiance $< 0.10\text{ nW}$.
  - If threshold is set to $< 0.20\text{ nW}$: **73 cells (73.0%)** meet the threshold in 2024.
- **Audit Verdict**: The 68% figure was an unverified text estimate. The correct verified empirical statistic is **51.0% of cells $< 0.10\text{ nW}$** and **73.0% of cells $< 0.20\text{ nW}$**.

### 2. Audit of Specific Suburban Expansion Claims:
We mapped coordinates for specific sub-centers and extracted their closest 5 km grid cell metrics:

| Location | Grid Cell ID | Row / Col | Coordinates | 2012 Mean | 2024 Mean | Absolute $\Delta$ | Growth % | Audit Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Sarjapur (BLR SE Fringe)** | `BLR_R03_C10` | R3, C10 | 12.853°N, 77.796°E | 3.83 nW | 14.38 nW | **+10.55 nW** | **+275.0%** | **CONFIRMED** (Massive expansion) |
| **Whitefield (BLR East)** | `BLR_R06_C09` | R6, C9 | 12.989°N, 77.752°E | 28.73 nW | 53.95 nW | **+25.22 nW** | **+87.8%** | **CONFIRMED** (Heavy commercial intensification) |
| **Electronic City (BLR South)** | `BLR_R03_C07` | R3, C7 | 12.854°N, 77.658°E | 26.81 nW | 49.61 nW | **+22.80 nW** | **+85.0%** | **CONFIRMED** (Substantial growth) |
| **Nanjangud (MYS South)** | `MYS_R01_C06` | R1, C6 | 12.103°N, 76.677°E | 9.41 nW | 10.10 nW | **+0.69 nW** | **+7.3%** | **CONFIRMED** (Moderate industrial growth) |
| **Yelahanka (BLR North Core)**| `BLR_R08_C05` | R8, C5 | 13.081°N, 77.568°E | 54.97 nW | 52.75 nW | **-2.22 nW** | **-4.0%** | **DISPROVED** (Yelahanka was already fully lit in 2012; did not experience >150% growth) |

### 3. Non-Causal Scientific Wording:
Low nocturnal radiance in Nilgiri–Bandipur reflects the absence of artificial lighting infrastructure and permanent settlements. It is an **observational spatial correlate** of protected wilderness zoning. We must not infer policy causality (i.e. that zoning *caused* the darkness, or that lack of light proves complete absence of ecological disturbance), as topography, road networks, and lack of electrical grid connectivity are confounding factors.

**Status**: **PASS WITH CAVEATS** (Empirical percentages and suburban claims corrected; non-causal language enforced).

---

## Section 9: Figure & Notebook Review

### 1. Inconsistencies in Figure Filenames vs. Content:
- **`figure_3_interannual_change_2023_2024.png`**:
  - *Observation*: The figure title displays *"Decadal Δ (2024 - 2012)"* and maps the 12-year spatial difference. However, the filename retains the label `2023_2024`.
  - *Correction*: The file accurately renders the 12-year decadal difference; its description must explicitly state that it visualizes $\Delta_{2024-2012}$.
- **`figure_4_seasonal_dynamics_march_vs_july.png`**:
  - *Observation*: The figure panels graph all 12 calendar months of 2024 (January through December). However, the filename retains the prototype label `march_vs_july`.
  - *Correction*: The file displays the full 12-month annual cycle; its caption must clarify that it covers all 12 months.

### 2. Notebook Execution & Relative Paths:
All seven notebooks in `notebooks/phase_2_nighttime_lights/` were audited:
- Every notebook executes cleanly from top to bottom with **zero errors**.
- All relative paths (`../../data/raw/...`, `../../geographical_boundaries/...`) work reliably.
- Code cells, tables, and plots are preserved in-place.

**Status**: **PASS WITH CAVEATS** (Figures verified valid in content; filename historical naming documented).

---

## Section 10: Manifest and Reproducibility Review

### Audit Target:
Verify that `dark_eco/data/metadata/viirs_dnb_manifest.csv` accounts for every asset.

### Verification Results:
- **Total Tracked Assets in Manifest**: **177 assets**.
- **Physical Files Missing**: **0**.
- **File Size Mismatches**: **0**.
- **Asset Breakdown**:
  - `raw_hdf5_granule`: 25 files (13 annual + 12 monthly).
  - `processed_cropped_raster`: 75 GeoTIFFs (25 time steps × 3 regions).
  - `processed_reprojected_raster`: 75 GeoTIFFs (conformal 500 m UTM Zone 43N).
  - `gridded_zonal_tabular`: 2 CSV files (`viirs_annual_5km_grid_metrics.csv` and `viirs_monthly_5km_grid_metrics.csv`).
- **Reproducibility**: Another researcher can clone the local repository, activate the Python virtual environment (`dark_eco/.venv`), and execute all seven notebooks without credential exposure.

**Status**: **PASS**

---

## Section 11: Summary of Discrepancies Found

1. **Nilgiri Cell Darkness Percentage**: Reported as 68% in prior text summary; verified empirical statistic is **51.0% of cells $< 0.10\text{ nW}$** and **73.0% of cells $< 0.20\text{ nW}$**.
2. **Suburban Growth Claim for Yelahanka**: The claim that Yelahanka grew by $>150\%$ is disproved for Yelahanka core (`BLR_R08_C05`, which stabilized at $\sim 53\text{ nW}$); the $>150\%$ growth occurred on the southeastern fringe (Sarjapur corridor, $+275\%$).
3. **Figure Filename Historical Artifacts**: `figure_3_interannual_change_2023_2024.png` renders decadal change (2024 vs 2012), and `figure_4_seasonal_dynamics_march_vs_july.png` renders the complete 12-month cycle of 2024.
4. **`_Num` Terminology**: Must be described as *Near-Nadir composite observations*, not *total clear-sky overpasses*.

---

## Section 12: Recommended Corrections

1. **Adopt Verified Grid Statistics**: Use $51.0\%$ (threshold $< 0.10\text{ nW}$) and $73.0\%$ (threshold $< 0.20\text{ nW}$) in all research reports.
2. **Refine Geographic Claims**: Cite Sarjapur (`BLR_R03_C10`, $+275\%$) as the primary example of peri-urban expansion rather than Yelahanka.
3. **Preserve Exact Figure Provenance**: Maintain existing figure files to avoid breaking links, but document their exact temporal scope in captions.
4. **Approve Phase 2 Sign-Off**: All core requirements (25 granules, 150 GeoTIFFs, 2 gridded tables, zero synthetic data, local execution) are verified. Phase 2 is scientifically sound.

---

### Audit Sign-Off
Phase 2 VIIRS deliverables have been audited and verified. The pipeline is ready for **Phase 3: GBIF Biodiversity Occurrence Data Collection, Inspection and Validation** upon user authorization.

