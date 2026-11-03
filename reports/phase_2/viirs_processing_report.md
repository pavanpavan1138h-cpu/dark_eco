# Dark Ecology Intelligence (DEI) — Phase 2: Nighttime Lights
# VIIRS-DNB Spatial Processing, Reprojection, and Multi-Temporal Zonal Aggregation Report

**Project**: Dark Ecology Intelligence (DEI) — ANN Problem-Based Learning  
**Date**: November 2026 (Full 25-Granule Archive Edition)  
**Phase**: Phase 2 — Nighttime Lights Data Collection, Inspection and Processing  
**Target Coordinate Systems**: WGS84 Geographic (`EPSG:4326`) and UTM Zone 43N (`EPSG:32643`)  
**Spatial Grids**: Native 500 m Pixel Raster and Project 5 km × 5 km Zonal Grid (300 Cells)  
**Archive Processed**: 25 Granules (13 Annual 2012–2024 + 12 Monthly Jan–Dec 2024)  
**Strict Integrity Rule**: 100% Genuine Satellite Radiometry — Zero Synthetic Data  

---

## 1. Executive Summary

This report documents the systematic data processing pipeline applied to the complete 25-granule archive of NASA Black Marble Collection 2 (`002`) observations covering Southern India (Tile `h25v07`).

The workflow was executed across Notebooks 05 and 06:
1. **Precise Boundary Cropping**: Sliced all 25 granules to the exact polygon bounds of Bengaluru, Mysuru, and Nilgiri–Bandipur (Option A), producing **75 WGS84 GeoTIFFs** in `data/processed/viirs_dnb/cropped/`.
2. **Conformal UTM Zone 43N Reprojection**: Reprojected all 75 rasters to UTM Zone 43N at an exact 500 m grid spacing, producing **75 UTM GeoTIFFs** in `data/processed/viirs_dnb/reprojected/`.
3. **5 km Grid Zonal Extraction**: Extracted multi-temporal zonal statistics across all 300 5 km grid cells (100 per region), exporting **two comprehensive research CSV tables** in `data/processed/viirs_dnb/gridded/`.

---

## 2. Regional Cropping Geometry and Slicing Bounds

Using exact floating point polygon bounds from `study_areas_summary.geojson` and 15-arcsecond coordinate vectors:

$$\text{Row} = \left\lfloor \frac{20.0^\circ - \text{Lat}}{0.00416667^\circ} \right\rfloor, \quad \text{Col} = \left\lfloor \frac{\text{Lon} - 70.0^\circ}{0.00416667^\circ} \right\rfloor$$

| Landscape | Polygon Bounding Coordinates [Lon, Lat] | Matrix Rows | Matrix Cols | Raster Dims | Edge Buffer |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Bengaluru** | `[77.3577°–77.8229°E, 12.7396°–13.1959°N]` | `[1633 : 1743]` | `[1766 : 1878]` | $110 \times 112$ | $> 230\text{ km}$ |
| **Mysuru** | `[76.4242°–76.8866°E, 12.0790°–12.5338°N]` | `[1792 : 1902]` | `[1542 : 1653]` | $110 \times 111$ | $> 220\text{ km}$ |
| **Nilgiri–Bandipur (Option A)** | `[76.3658°–76.8270°E, 11.4286°–11.8832°N]` | `[1949 : 2058]` | `[1528 : 1639]` | $109 \times 111$ | $> 155\text{ km}$ |

*Option A Boundary Note*: The approved Option A boundary was strictly preserved, completely covering Bandipur National Park, Mudumalai Tiger Reserve, and the Wayanad wildlife corridor.

---

## 3. Reprojection to UTM Zone 43N (`EPSG:32643`)

- **Resampling Method**: Bilinear interpolation (`Resampling.bilinear`) for continuous radiance values; nearest-neighbour for categorical flags.
- **Pixel Spacing**: Exactly 500.0 m × 500.0 m.
- **NoData Value**: `-999.9` preserved across all reprojections.
- **Total Processed Rasters**: 150 GeoTIFFs (75 WGS84 + 75 UTM Zone 43N).

---

## 4. Multi-Temporal 5 km Zonal Grid Aggregation

For each of the 300 5 km grid cells ($25\text{ km}^2$, containing $10 \times 10 = 100$ pixels), zonal metrics were extracted across all 25 time steps:

### Generated Zonal Datasets in `data/processed/viirs_dnb/gridded/`:
1. `viirs_annual_5km_grid_metrics.csv` (300 rows, 42 columns):
   - Cell ID, region, row, col, centroid lon/lat, area (25 km²).
   - 13 years of annual metrics (2012–2024): `mean_rad`, `valid_px`.
   - Detailed metrics for 2012 and 2024: `median_rad`, `max_rad`, `std_rad`.
   - Decadal metrics: Absolute change ($\Delta_{2024-2012}$) and relative growth percentage ($\%$).
2. `viirs_monthly_5km_grid_metrics.csv` (300 rows, 42 columns):
   - Cell ID, region, row, col, centroid lon/lat.
   - All 12 months of 2024: `mean_rad`, `cov_pct`, `valid_px`.

---

## 5. Decadal Illumination Evolution Across Landscapes (2012 vs 2024)

```
========================================================================================
                      DECADAL NOCTURNAL ILLUMINATION EVOLUTION (2012–2024)
========================================================================================
Landscape Region           2012 Mean Rad      2024 Mean Rad       Decadal Δ       Growth %
----------------------------------------------------------------------------------------
Bengaluru (Urban)         18.01 nW/cm²/sr    26.79 nW/cm²/sr    +8.78 nW/cm²/sr    +48.7%
Mysuru (Transitional)      2.14 nW/cm²/sr     3.61 nW/cm²/sr    +1.47 nW/cm²/sr    +68.7%
Nilgiri-Bandipur (Forest)  0.28 nW/cm²/sr     0.29 nW/cm²/sr    +0.01 nW/cm²/sr     +3.6%
========================================================================================
```

- **Urban Core Sprawl**: Bengaluru experienced steady outward sprawl (+48.7% regional mean), with peripheral cells along the Electronic City and Whitefield corridors increasing by $>150\%$.
- **Transitional Accretion**: Mysuru expanded along the southern industrial corridor (+68.7% growth).
- **Wilderness Preservation**: Nilgiri–Bandipur remained insulated (regional mean change $+0.01\text{ nW}$), with 68% of cells remaining below $0.10\text{ nW}$.

---

## 6. Data Integrity and Verification

- **Zero Synthetic Data**: Every value in the 150 GeoTIFFs and 2 gridded CSVs originates directly from genuine satellite radiometry.
- **Traceability**: All 177 research assets are indexed in `data/metadata/viirs_dnb_manifest.csv`.
