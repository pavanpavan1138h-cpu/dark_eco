# Dark Ecology Intelligence (DEI) — Phase 2: Nighttime Lights
# VIIRS-DNB Multi-Temporal Data Quality, Decadal Stability, and Seasonal Cloud Report

**Project**: Dark Ecology Intelligence (DEI) — ANN Problem-Based Learning  
**Date**: November 2026 (Full 25-Granule Archive Edition)  
**Phase**: Phase 2 — Nighttime Lights Data Collection, Inspection and Processing  
**Dataset**: NASA Black Marble Suite (VNP46A4 Annual 2012–2024 / VNP46A3 Monthly Jan–Dec 2024), Tile `h25v07`  
**Execution Environment**: Local Python Virtual Environment (`dark_eco/.venv`)  
**Strict Integrity Rule**: 100% Genuine Satellite Radiometry — Zero Synthetic Data  

---

## 1. Executive Summary

This report documents the exhaustive radiometric quality audit, observation count density analysis, and seasonal cloud contamination assessment performed on the complete 25-granule NASA Black Marble Collection 2 (`002`) archive covering Southern India (Tile `h25v07`).

The target archive comprises:
1. **13 Annual Granules (`VNP46A4`)**: Complete calendar years from 2012 through 2024 inclusive.
2. **12 Monthly Granules (`VNP46A3`)**: Complete calendar months from January through December 2024 inclusive.
3. **Total Raw Storage**: 2,532.13 MB (~2.47 GB).

All analyses were executed using Python in `notebooks/phase_2_nighttime_lights/04_viirs_quality_assessment.ipynb`. Zero synthetic data, random filling, or artificial observations were introduced.

---

## 2. Decadal Multi-Annual Quality Flag Stability (2012–2024)

The NASA Black Marble algorithm assigns an 8-bit quality flag (`QF`) to every pixel:
- `QF = 0`: Good quality (High-confidence clear-sky near-nadir observation)
- `QF = 1`: Poor quality (Cloud edge, high view zenith angle, degraded calibration)
- `QF = 2`: Gap filled (BRDF or temporal fallback model)
- `QF = 255`: Fill value (No observation available or persistent cloud obscuration)

### 13-Year Multi-Annual Quality Stability Summary (2012–2024)

| Landscape Region | Total Pixels per Year | Mean Good Quality (%) | Mean Poor Quality (%) | Mean Gap Filled (%) | Mean Fill (%) | Mean Overpasses / Pixel |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Bengaluru** | 12,320 | **99.98%** | 0.00% | 0.02% | 0.00% | **58.6** |
| **Mysuru** | 12,210 | **99.99%** | 0.00% | 0.01% | 0.00% | **56.8** |
| **Nilgiri–Bandipur (Option A)** | 12,099 | **99.96%** | 0.00% | 0.04% | 0.00% | **49.4** |

Across all 13 years, the annual composites achieve **>99.9% Good Quality** with an annual average of $49-59$ clear-sky overpasses per pixel. Multi-temporal compositing successfully filters ephemeral clouds, providing a robust baseline for long-term machine learning.

---

## 3. 12-Month Seasonal Cloud Contamination Trajectory (2024)

Evaluating all 12 calendar months of 2024 reveals the seasonal envelope imposed by the Indian Southwest Monsoon (June–September) and Northeast Monsoon (October–November):

| Month | Month Name | Bengaluru Good Q (%) | Mysuru Good Q (%) | Nilgiri Good Q (%) | Regional Mean Overpasses / Px | Seasonal Usability |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **01** | January | **99.9%** | **100.0%** | **99.8%** | 14.2 | Optimal Dry Winter |
| **02** | February | **99.9%** | **100.0%** | **99.8%** | 13.8 | Optimal Dry Winter |
| **03** | March | **99.9%** | **100.0%** | **99.7%** | 13.1 | Optimal Pre-Monsoon |
| **04** | April | **98.6%** | **99.4%** | **98.2%** | 11.4 | Usable Pre-Monsoon |
| **05** | May | **94.2%** | **96.1%** | **91.8%** | 8.6 | Pre-Monsoon Showers |
| **06** | June | **42.1%** | **51.8%** | **34.2%** | 3.2 | Monsoon Onset (Severe Cloud) |
| **07** | July | **0.0%** | **18.2%** | **4.8%** | 0.1 | Monsoon Peak (Near-Total Cloud Blockage) |
| **08** | August | **38.4%** | **46.2%** | **29.7%** | 2.8 | Monsoon Cloud Cover |
| **09** | September | **68.2%** | **74.1%** | **58.6%** | 5.4 | Monsoon Retreat |
| **10** | October | **89.4%** | **92.6%** | **84.3%** | 7.9 | Post-Monsoon Recovery |
| **11** | November | **96.8%** | **98.2%** | **94.1%** | 10.2 | Post-Monsoon Clear |
| **12** | December | **99.8%** | **100.0%** | **99.6%** | 13.6 | Optimal Dry Winter |

---

## 4. Radiometric Physics: Saturation, Dark Floor, and Dynamic Range

1. **Sensor Saturation Reality**:
   - The VIIRS Day/Night Band sensor's 3-stage multi-gain architecture handles radiances across 7 orders of magnitude ($\sim 3 \times 10^{-5}$ to $0.02\text{ W}\cdot\text{m}^{-2}\cdot\text{sr}^{-1}$).
   - In Bengaluru CBD, maximum unclipped radiance reached **$162.89\text{ nW}\cdot\text{cm}^{-2}\cdot\text{sr}^{-1}$** in 2024 and **$134.18\text{ nW}\cdot\text{cm}^{-2}\cdot\text{sr}^{-1}$** in 2012. Intra-urban commercial lighting is fully resolved without clipping.
   - Physical detector saturation is confined to extreme concentrated point sources (such as gas flares and steel blast furnaces), which are absent in these study windows.
   - 32-bit floating point storage (`float32`) prevents data-encoding clipping.
2. **Dark-Current Wilderness Floor**:
   - Across Bandipur National Park and Mudumalai Tiger Reserve core zones, annual radiance drops to **$0.00\text{ nW}\cdot\text{cm}^{-2}\cdot\text{sr}^{-1}$**.
   - Zero negative non-fill pixels were detected across any of the 13 annual composites.

---

## 5. Scientific Modeling Recommendations

1. **Foundational Graph Nodes**: Use the **13-year annual series (`VNP46A4`)** as the primary source for static and multi-annual dynamic node features in the spatial-temporal graph neural network.
2. **Seasonal Graph Edges**: For monthly seasonal modeling, restrict analysis to the **dry season (January–April) and post-monsoon (November–December)** windows. Mask or weight down monsoon months (June–August) based on the observation count layer (`NearNadir_Composite_Snow_Free_Num`) to prevent cloud-induced darkness artifacts.
