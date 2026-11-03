"""Geographical framework utilities for the DEI project.

Defines the three provisional 50 km x 50 km study windows and builds the
common 5 km x 5 km grid. All metric work is done in WGS 84 / UTM zone 43N
(EPSG:32643) using `pyproj`; outputs are reprojected to WGS 84 (EPSG:4326)
for GeoJSON storage (RFC 7946 requires WGS 84 longitude/latitude).

No observational data is created here - only geometric reference frames.
"""
from __future__ import annotations

import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import box

UTM_CRS = "EPSG:32643"   # WGS 84 / UTM zone 43N (central meridian 75 deg E)
WGS84_CRS = "EPSG:4326"
CELL_SIZE_M = 5_000      # 5 km
CELLS_PER_SIDE = 10      # 10 x 10 cells = 50 km x 50 km
SNAP_M = 1_000           # window origin snapped to whole kilometres

# Window centres are chosen anchor points (an ASSUMPTION/design choice,
# documented in reports/phase_1/geographical_framework.md).
REGIONS = {
    "bengaluru": {
        "prefix": "BLR",
        "name": "Bengaluru urban-peri-urban window",
        "landscape_type": "highly urbanised",
        "anchor": "Central Bengaluru (Vidhana Soudha area)",
        "center_lat": 12.9716,
        "center_lon": 77.5946,
    },
    "mysuru": {
        "prefix": "MYS",
        "name": "Mysuru peri-urban / transitional window",
        "landscape_type": "peri-urban and transitional",
        "anchor": "Mysuru city centre (Mysuru Palace area)",
        "center_lat": 12.3051,
        "center_lon": 76.6551,
    },
    "nilgiri_bandipur": {
        "prefix": "NB",
        "name": "Bandipur-Mudumalai forest window (Nilgiri-Bandipur)",
        "landscape_type": "forest and protected-area",
        "anchor": "Karnataka-Tamil Nadu border near Moyar river (Bandipur/Mudumalai junction)",
        "center_lat": 11.6600,
        "center_lon": 76.6000,
    },
}

_to_utm = Transformer.from_crs(WGS84_CRS, UTM_CRS, always_xy=True)


def window_bounds_utm(center_lat: float, center_lon: float) -> tuple[float, float, float, float]:
    """Return (minx, miny, maxx, maxy) of the 50 km window in UTM 43N metres.

    The south-west corner is snapped to the nearest whole kilometre so that
    grid-cell edges fall on round metric coordinates.
    """
    cx, cy = _to_utm.transform(center_lon, center_lat)
    half = CELL_SIZE_M * CELLS_PER_SIDE / 2
    minx = round((cx - half) / SNAP_M) * SNAP_M
    miny = round((cy - half) / SNAP_M) * SNAP_M
    side = CELL_SIZE_M * CELLS_PER_SIDE
    return minx, miny, minx + side, miny + side


def build_window(region_id: str) -> gpd.GeoDataFrame:
    """One-row GeoDataFrame (UTM 43N) holding the study-window polygon."""
    r = REGIONS[region_id]
    minx, miny, maxx, maxy = window_bounds_utm(r["center_lat"], r["center_lon"])
    return gpd.GeoDataFrame(
        [{
            "region_id": region_id,
            "region_name": r["name"],
            "landscape_type": r["landscape_type"],
            "anchor": r["anchor"],
            "utm_min_x": minx, "utm_min_y": miny,
            "utm_max_x": maxx, "utm_max_y": maxy,
            "n_cells": CELLS_PER_SIDE ** 2,
            "cell_size_m": CELL_SIZE_M,
        }],
        geometry=[box(minx, miny, maxx, maxy)],
        crs=UTM_CRS,
    )


def build_grid(region_id: str) -> gpd.GeoDataFrame:
    """10 x 10 GeoDataFrame (UTM 43N) of 5 km cells.

    Cell IDs follow `{PREFIX}_R{row:02d}_C{col:02d}`; row 01 is the southern-most
    row and column 01 the western-most column.
    """
    r = REGIONS[region_id]
    minx, miny, _, _ = window_bounds_utm(r["center_lat"], r["center_lon"])
    rows = []
    for i in range(CELLS_PER_SIDE):
        for j in range(CELLS_PER_SIDE):
            x0 = minx + j * CELL_SIZE_M
            y0 = miny + i * CELL_SIZE_M
            rows.append({
                "cell_id": f"{r['prefix']}_R{i + 1:02d}_C{j + 1:02d}",
                "region_id": region_id,
                "row": i + 1,
                "col": j + 1,
                "utm_min_x": x0, "utm_min_y": y0,
                "utm_max_x": x0 + CELL_SIZE_M, "utm_max_y": y0 + CELL_SIZE_M,
                "geometry": box(x0, y0, x0 + CELL_SIZE_M, y0 + CELL_SIZE_M),
            })
    gdf = gpd.GeoDataFrame(rows, crs=UTM_CRS)
    cent = gdf.geometry.centroid.to_crs(WGS84_CRS)
    gdf["centroid_lon"] = cent.x.round(6)
    gdf["centroid_lat"] = cent.y.round(6)
    gdf["area_km2"] = (gdf.geometry.area / 1e6).round(3)
    return gdf

