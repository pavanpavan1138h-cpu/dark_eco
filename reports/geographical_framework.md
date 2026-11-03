# Dark Ecology Intelligence (DEI) — Geographical Framework Report

---

## 1. Executive Summary

This report establishes the spatial architecture and geographic boundaries for the **Dark Ecology Intelligence (DEI)** project across three representative landscapes in Southern India:
1. **Bengaluru Urban-Periurban Landscape** (High-intensity nocturnal lighting and hyper-urbanization).
2. **Mysuru Peri-Urban & Transitional Landscape** (Intermediate lighting gradient with intensive agricultural matrix).
3. **Nilgiri–Bandipur Forest & Corridor Landscape** (Low-lighting wilderness baseline with critical localized anthropogenic frontiers).

A standardized **5 km × 5 km regular grid** projected in **UTM Zone 43N (EPSG:32643)** is established across all three regions, producing **100 grid cells per landscape (300 cells total, 7,500 km² total coverage)**. This unified framework enables direct cross-landscape comparative modeling while accommodating diverse land-cover types, administrative borders, and protected area jurisdictions.

---

## 2. Landscape Delineation & Scientific Justifications

### 2.1 Landscape 1: Bengaluru Urban-Periurban Landscape

| Attribute | Specification |
| :--- | :--- |
| **Primary Classification** | Megacity Urban Core, Peri-Urban Fringe, and Lake/Grassland Basins |
| **Centroid (WGS84)** | 12.9716° N, 77.5946° E (Vidhana Soudha / Central Bengaluru) |
| **Latitude Bounds** | 12.7396° N to 13.1959° N (~50.5 km) |
| **Longitude Bounds** | 77.3577° E to 77.8229° E (~50.4 km) |
| **UTM Zone 43N Bounds** | Easting: 756,000 m – 806,000 m; Northing: 1,410,000 m – 1,460,000 m |
| **Total Area** | 2,500 km² (10 × 10 cells of 25 km² each) |
| **Administrative References** | Bruhat Bengaluru Mahanagara Palike (BBMP Master Plan 2031); Bangalore Metropolitan Region Development Authority (BMRDA); Survey of India OSM Rel: 7953487. |

#### Scientific Justification & Landscape Elements
- **Urban Core & Commercial Centers**: Encompasses the high-density municipal core (Majestic, MG Road, Indiranagar, Koramangala) where DMSP-OLS historical sensors experience digital saturation (DN=63) and VIIRS-DNB radiances peak above 80 nW/cm²·sr.
- **High-Tech & Industrial Corridors**: Captures the eastward expansion along the Outer Ring Road, Whitefield IT hub, and south-eastern Electronic City corridors.
- **Peri-Urban & Agricultural Transition**: Northern agricultural catchments of Hesaraghatta and Yelahanka, extending toward Devanahalli and the Kempegowda International Airport corridor.
- **Ecological Interfaces & Green Buffers**: Integrates fragmented urban wetland chains (Bellandur, Varthur, Hebbal, and Jakkur lakes) and terminates in the south at the northern buffer and eco-sensitive zone of **Bannerghatta National Park (BNP)**, establishing a direct urban-wildland interface.

---

### 2.2 Landscape 2: Mysuru Peri-Urban & Transitional Landscape

| Attribute | Specification |
| :--- | :--- |
| **Primary Classification** | Historic Urban Core, Sub-urban Industrial Belts, Agrarian & Riparian Matrix |
| **Centroid (WGS84)** | 12.3051° N, 76.6551° E (Mysuru Palace / Heritage Core) |
| **Latitude Bounds** | 12.0790° N to 12.5338° N (~50.3 km) |
| **Longitude Bounds** | 76.4242° E to 76.8866° E (~50.2 km) |
| **UTM Zone 43N Bounds** | Easting: 655,000 m – 705,000 m; Northing: 1,336,000 m – 1,386,000 m |
| **Total Area** | 2,500 km² (10 × 10 cells of 25 km² each) |
| **Administrative References** | Mysuru City Corporation (MCC); Mysuru Urban Development Authority (MUDA Master Plan 2031); Karnataka State Remote Sensing Applications Centre (KSRSAC). |

#### Scientific Justification & Landscape Elements
- **Intermediate ALAN Gradient**: Mysuru represents an essential transitional landscape archetype in the Deccan plateau. Unlike Bengaluru's continuous high-radiance urban sprawl, Mysuru features a bounded, medium-intensity nocturnal lighting core surrounded by extensive darkness.
- **Chamundi Hill Reserve Forest**: An isolated 17 km² sacred grove and dry deciduous hill forest directly adjoining the urban fabric, providing a high-contrast ecological island subject to circumferential skyglow.
- **Riparian & Wetland Corridors**: Integrates the Cauvery River basin to the north, including the **Ranganathittu Bird Sanctuary** (Ramsar Site, WDPA ID 14282), and the Kabini River basin to the south, supporting large populations of colonial waterbirds, bats, and aquatic invertebrates.
- **Agricultural Matrix**: Surrounded by flood-irrigated sugarcane and paddy agro-ecosystems (Srirangapatna, Nanjangud highway corridor), representing the typical peri-urban rural-urban interface of Southern India.

---

### 2.3 Landscape 3: Nilgiri–Bandipur Forest & Ecological Corridor

| Attribute | Specification |
| :--- | :--- |
| **Primary Classification** | Protected Tropical Forest, Tiger Reserve, and Wildlife Corridor Bottleneck |
| **Centroid (WGS84)** | 11.6600° N, 76.6000° E (Moyar River Gorge / Interstate Boundary) |
| **Latitude Bounds** | 11.4286° N to 11.8832° N (~50.3 km) |
| **Longitude Bounds** | 76.3658° E to 76.8270° E (~50.2 km) |
| **UTM Zone 43N Bounds** | Easting: 649,000 m – 699,000 m; Northing: 1,264,000 m – 1,314,000 m |
| **Total Area** | 2,500 km² (10 × 10 cells of 25 km² each) |
| **Protected Area References** | Bandipur National Park & Tiger Reserve (WDPA ID 862); Mudumalai Tiger Reserve (WDPA ID 863); Sigur Plateau Elephant Corridor; NTCA Notifications. |

#### Scientific Justification & Critical Boundary Delineation
- **Explicit Distinction from Nilgiri Biosphere Reserve (NBR)**: The Nilgiri Biosphere Reserve spans over 5,520 km² across Karnataka, Kerala, and Tamil Nadu, containing vastly different biomes ranging from wet evergreen rainforests in Silent Valley to 2,600 m high-altitude montane shola-grasslands in Mukurthi and Upper Nilgiris. **We explicitly do NOT treat the entire NBR as equivalent to Bandipur National Park.**
- **The Defined Study Landscape**: Our framework strictly defines the **Bandipur–Mudumalai Transboundary Tiger Landscape and Moyar/Sigur Corridor**. This region encompasses the contiguous dry and moist deciduous forest tracts of:
  1. **Bandipur National Park** (Chamarajanagar District, Karnataka, ~874 km²).
  2. **Mudumalai Tiger Reserve** (Nilgiris District, Tamil Nadu, ~321 km²).
  3. **The Moyar River Gorge and Sigur Plateau Corridor**: The vital ecological link connecting the Western Ghats to the Eastern Ghats (Biligirirangana Hills and Sathyamangalam Tiger Reserve), which forms the world's largest contiguous Asian Elephant (*Elephas maximus*) and Bengal Tiger (*Panthera tigris*) population.
- **Anthropogenic ALAN Frontiers in Wilderness**: While predominantly characterized by dark skies (<0.1 nW/cm²·sr), this landscape contains critical, localized nocturnal light sources:
  - **National Highway 766** (Mysuru–Gundlupet–Sulthan Bathery) and **National Highway 181** (Gundlupet–Masinagudi–Ooty), which bisect core tiger habitat and historically carried severe night traffic prior to partial night-traffic bans.
  - **Commercial Ecotourism Clusters**: High-density resort lighting in Masinagudi, Bokkapuram, and Mangala along the forest fringe.
  - **Agrarian Fringes**: Solar/electric fencing and compound floodlighting around agricultural settlements in Gundlupet taluk.

---

## 3. Common Spatial Framework

```
+-------------------------------------------------------------------------+
|                       COMMON SPATIAL FRAMEWORK                          |
|                                                                         |
|  Geodetic Storage CRS:  WGS 84 (EPSG:4326)                             |
|  Projected Metric CRS:  UTM Zone 43N (EPSG:32643)                       |
|  Grid Resolution:      5.0 km x 5.0 km (25.0 km² per cell)              |
|  Landscape Dimension:  50.0 km x 50.0 km (10 x 10 cells = 100 cells)    |
|                                                                         |
|     Bengaluru (BLR)            Mysuru (MYS)         Nilgiri-Bandipur    |
|   100 Cells (2,500 km²)    100 Cells (2,500 km²)   100 Cells (2,500 km²)|
|   [BLR_R01_C01..R10_C10]   [MYS_R01_C01..R10_C10]  [NB_R01_C01..R10_C10]|
+-------------------------------------------------------------------------+
```

### 3.1 Coordinate Reference System Selection

1. **Projected Coordinate Reference System**: **WGS 84 / UTM Zone 43N (EPSG:32643)**
   - *Rationale*: All three landscapes lie between 76°20' E and 77°50' E, fitting within the central longitudinal strip of UTM Zone 43N (Central Meridian: 75°00' E).
   - *Advantage*: Enables true metric Euclidean calculations (exact 5,000 m × 5,000 m spacing, accurate buffer distances, metric slope and aspect calculation from DEM).
   - *Distortion*: Scale factor distortion across all study areas is less than 0.08%, which is negligible for regional ecological modeling.
2. **Geographic Storage CRS**: **WGS 84 (EPSG:4326)**
   - *Rationale*: All GeoJSON and vector exports are encoded in standard decimal degrees (`urn:ogc:def:crs:OGC:1.3:CRS84`) to guarantee direct rendering across QGIS, ArcGIS, Google Earth Engine, Leaflet, and Python (`geopandas`, `shapely`, `folium`).

### 3.2 Cell Identification and Schema

Every grid cell across the 300-cell system is indexed by a deterministic, human-readable identifier:
- Formula: `{PREFIX}_R{ROW:02d}_C{COL:02d}`
  - Bengaluru: `BLR_R01_C01` (southwest) to `BLR_R10_C10` (northeast)
  - Mysuru: `MYS_R01_C01` (southwest) to `MYS_R10_C10` (northeast)
  - Nilgiri-Bandipur: `NB_R01_C01` (southwest) to `NB_R10_C10` (northeast)

Attributes attached to each cell feature:
- `cell_id`: Unique identifier (string).
- `region_id`: Region tag (`bengaluru`, `mysuru`, `nilgiri_bandipur`).
- `row_index` & `col_index`: Matrix positions (1 to 10).
- `centroid_lat` & `centroid_lon`: Cell centroid in WGS84 decimal degrees.
- `utm_min_east`, `utm_max_east`, `utm_min_north`, `utm_max_north`: Metric bounding envelope.
- `area_km2`: Nominal cell area (25.0 km²).

### 3.3 Handling Complex Spatial Features

1. **Water Bodies and River Basins**:
   - Several grid cells intersect significant inland reservoirs (e.g. Krishnarajasagara / KRS and Kabini Reservoir in Mysuru; Bellandur and Varthur lakes in Bengaluru; Moyar reservoir and river in Bandipur).
   - *Handling*: In Phase 5, water body masks derived from **ESA WorldCover (Class 80)** and Copernicus DEM water masks will compute `land_area_fraction` for each cell. Cells with high water fractions will not be discarded; instead, water percentage will serve as a continuous structural covariate.
2. **Missing Satellite Observations (Cloud Masking)**:
   - Southwest Monsoon (June–September) causes frequent cloud cover in optical and nighttime satellite sensors, particularly along the Nilgiri slopes.
   - *Handling*: Monthly nighttime light products (VIIRS-DNB / Black Marble) will use cloud-free coverage counts (`cf_cvg`) to weight observations. Cells with zero cloud-free nights in a given monsoon month will be imputed using seasonal baseline spline interpolation rather than treated as true dark values.
3. **Boundary Clipping and Edge Effects**:
   - Grid cells along the outer border of the 50 km × 50 km window will retain their full 5 km × 5 km geometry. Rather than irregularly clipping cells along administrative lines, all external predictor rasters (ERA5-Land, WorldPop, Hansen GFC) will be sampled over the full cell extent.
   - Spatial graph adjacency matrices for Graph Neural Networks (ST-GNNs) will use Queen contiguity (8 neighbors) and Rook contiguity (4 neighbors) with boundary padding.

---

## 4. Evaluation: 50 km × 50 km Fixed Window vs. Administrative / Ecological Boundaries

| Criterion | 50 km × 50 km Fixed Regular Window (Recommended) | Pure Administrative Boundary (BBMP / MCC / Taluks) | Pure Protected Area Boundary (Bandipur Core Only) |
| :--- | :--- | :--- | :--- |
| **Cross-Landscape Comparability** | **Optimal**: Identical sample size ($N=100$), identical spatial graph topology, identical area ($2,500\text{ km}^2$). | **Poor**: BBMP is ~712 km², Mysuru MCC is ~128 km²; massive geometric disparity. | **Poor**: Bandipur NP is ~874 km²; irregular boundary excludes neighboring Mudumalai and corridor. |
| **Interface Capture** | **Superior**: Captures urban-to-rural and forest-to-agricultural transitions. | **Fails**: Excludes peri-urban rural growth and agricultural matrix outside city limits. | **Fails**: Completely misses fringe road lighting, ecotourism resorts, and forest-edge settlements. |
| **Neural Network Tensor Shapes** | **Ideal**: Regular $10 \times 10$ spatial grid enables standard 2D convolution, Graph Convolutional Networks (GCNs), and grid adjacency matrices. | **Difficult**: Ragged graph matrices; varying node counts require complex masked graph pooling. | **Difficult**: Highly fragmented boundary causes extreme boundary edge artifacts. |
| **Limitation** | Includes some external agricultural landscape outside primary municipal interest. | High political relevance for city-specific administrative reports. | Direct administrative authority under Karnataka Forest Department only. |

**Conclusion**: The **50 km × 50 km regular window** is mathematically and ecologically superior for comparative Spatio-Temporal Graph Neural Network modeling, while administrative and protected area vectors will be overlaid to compute jurisdictional summary statistics.

---

## 5. Generated Boundary and Grid Assets

The following verified GeoJSON boundary files have been generated in `dark_eco/geographical_boundaries/`:
- [`study_areas_summary.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/study_areas_summary.geojson)
- [`bengaluru_study_area.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/bengaluru_study_area.geojson)
- [`mysuru_study_area.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/mysuru_study_area.geojson)
- [`nilgiri_bandipur_study_area.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/nilgiri_bandipur_study_area.geojson)
- [`bengaluru_5km_grid.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/bengaluru_5km_grid.geojson)
- [`mysuru_5km_grid.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/mysuru_5km_grid.geojson)
- [`nilgiri_bandipur_5km_grid.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/nilgiri_bandipur_5km_grid.geojson)
- [`all_regions_5km_grid.geojson`](file:///Users/apple/Documents/5th%20sem%20el/ANN_PBL/dark_eco/geographical_boundaries/all_regions_5km_grid.geojson)

