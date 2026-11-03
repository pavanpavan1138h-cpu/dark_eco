#!/usr/bin/env python3
"""
Dark Ecology Intelligence (DEI) - Phase 1 Setup
Script: generate_boundaries_and_grids.py

Generates mathematically rigorous GIS-compatible GeoJSON boundaries and
common 5 km x 5 km spatial grid cells for the three study landscapes:
  1. Bengaluru (Urbanized landscape)
  2. Mysuru (Peri-urban / transitional landscape)
  3. Nilgiri-Bandipur (Protected forest / corridor landscape)

CRS Framework:
  - Projected Metric CRS: UTM Zone 43N (EPSG:32643) for exact 5,000m x 5,000m spacing
  - Geographic Storage CRS: WGS 84 (EPSG:4326) for universal GeoJSON compatibility
"""

import json
import math
import os

# --- Geodesic & UTM Projection Helpers (UTM Zone 43N, WGS84) ---
WGS84_A = 6378137.0
WGS84_F = 1 / 298.257223563
WGS84_E2 = 2 * WGS84_F - WGS84_F**2
WGS84_E_PRIME2 = WGS84_E2 / (1 - WGS84_E2)
UTM_K0 = 0.9996
UTM_LON0 = 75.0  # Central Meridian for UTM Zone 43N

def latlon_to_utm43n(lat, lon):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    lon0_rad = math.radians(UTM_LON0)
    
    N = WGS84_A / math.sqrt(1 - WGS84_E2 * math.sin(lat_rad)**2)
    T = math.tan(lat_rad)**2
    C = WGS84_E_PRIME2 * math.cos(lat_rad)**2
    A = math.cos(lat_rad) * (lon_rad - lon0_rad)
    
    M = WGS84_A * (
        (1 - WGS84_E2/4 - 3*WGS84_E2**2/64 - 5*WGS84_E2**3/256) * lat_rad
        - (3*WGS84_E2/8 + 3*WGS84_E2**2/32 + 45*WGS84_E2**3/1024) * math.sin(2*lat_rad)
        + (15*WGS84_E2**2/256 + 45*WGS84_E2**3/1024) * math.sin(4*lat_rad)
        - (35*WGS84_E2**3/3072) * math.sin(6*lat_rad)
    )
             
    easting = 500000.0 + UTM_K0 * N * (
        A + (1 - T + C) * A**3 / 6 + (5 - 18*T + T**2 + 72*C - 58*WGS84_E_PRIME2) * A**5 / 120
    )
    northing = UTM_K0 * (
        M + N * math.tan(lat_rad) * (
            A**2 / 2 + (5 - T + 9*C + 4*C**2) * A**4 / 24
            + (61 - 58*T + T**2 + 600*C - 330*WGS84_E_PRIME2) * A**6 / 720
        )
    )
    return easting, northing

def utm43n_to_latlon(easting, northing):
    x = easting - 500000.0
    y = northing
    
    M = y / UTM_K0
    mu = M / (WGS84_A * (1 - WGS84_E2/4 - 3*WGS84_E2**2/64 - 5*WGS84_E2**3/256))
    e1 = (1 - math.sqrt(1 - WGS84_E2)) / (1 + math.sqrt(1 - WGS84_E2))
    
    phi1_rad = (
        mu + (3*e1/2 - 27*e1**3/32) * math.sin(2*mu)
        + (21*e1**2/16 - 55*e1**4/32) * math.sin(4*mu)
        + (151*e1**3/96) * math.sin(6*mu)
        + (1097*e1**4/512) * math.sin(8*mu)
    )
                
    N1 = WGS84_A / math.sqrt(1 - WGS84_E2 * math.sin(phi1_rad)**2)
    T1 = math.tan(phi1_rad)**2
    C1 = WGS84_E_PRIME2 * math.cos(phi1_rad)**2
    R1 = WGS84_A * (1 - WGS84_E2) / ((1 - WGS84_E2 * math.sin(phi1_rad)**2)**1.5)
    D = x / (N1 * UTM_K0)
    
    lat_rad = phi1_rad - (N1 * math.tan(phi1_rad) / R1) * (
        D**2 / 2 - (5 + 3*T1 + 10*C1 - 4*C1**2 - 9*WGS84_E_PRIME2) * D**4 / 24
        + (61 + 90*T1 + 298*C1 + 45*T1**2 - 252*WGS84_E_PRIME2 - 3*C1**2) * D**6 / 720
    )
    lon_rad = math.radians(UTM_LON0) + (
        D - (1 + 2*T1 + C1) * D**3 / 6
        + (5 - 2*C1 + 28*T1 - 3*C1**2 + 8*WGS84_E_PRIME2 + 24*T1**2) * D**5 / 120
    ) / math.cos(phi1_rad)
    
    return round(math.degrees(lat_rad), 6), round(math.degrees(lon_rad), 6)

# Landscape Definitions (50km x 50km centered around key ecological/urban landmarks)
STUDY_REGIONS = {
    "bengaluru": {
        "region_id": "bengaluru",
        "region_name": "Bengaluru Urban-Periurban Landscape",
        "prefix": "BLR",
        "landscape_type": "Highly Urbanised & Peri-urban Gradient",
        "center_lat": 12.9716,
        "center_lon": 77.5946,
        "description": "Encompasses BBMP urban core, IT corridors (Whitefield, Electronic City), Hesaraghatta catchment, and northern buffer of Bannerghatta NP.",
        "scientific_rationale": "Represents the extreme high end of the regional ALAN gradient; rapid urban expansion replacing vegetation and waterbodies over 1992-2024."
    },
    "mysuru": {
        "region_id": "mysuru",
        "region_name": "Mysuru Peri-Urban & Transitional Landscape",
        "prefix": "MYS",
        "landscape_type": "Peri-urban & Transitional Matrix",
        "center_lat": 12.3051,
        "center_lon": 76.6551,
        "description": "Encompasses Mysuru city core, Chamundi Hill Reserve Forest, Srirangapatna agrarian corridor, Cauvery/Kabini agricultural valleys.",
        "scientific_rationale": "Represents the intermediate ALAN transitional gradient; suburbanization and agrarian matrix with moderate baseline lighting."
    },
    "nilgiri_bandipur": {
        "region_id": "nilgiri_bandipur",
        "region_name": "Nilgiri-Bandipur Forest & Corridor Landscape",
        "prefix": "NB",
        "landscape_type": "Protected Forest & Ecological Corridor",
        "center_lat": 11.6600,
        "center_lon": 76.6000,
        "description": "Bandipur National Park (Karnataka) contiguous with Mudumalai Tiger Reserve (Tamil Nadu) and Moyar/Sigur elephant corridor. Explicitly excludes the high Nilgiri plateau to focus on the dry/moist deciduous tiger-elephant corridor.",
        "scientific_rationale": "Represents the low-ALAN wilderness baseline with critical localized light pollution frontiers (highway night traffic, tourist lodge clusters, forest-edge villages)."
    }
}

GRID_CELL_SIZE_METERS = 5000  # 5 km x 5 km
NUM_CELLS_PER_SIDE = 10       # 10 x 10 grid = 100 cells per region (50km x 50km = 2,500 km2)

def generate_spatial_grid_and_boundaries(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    all_grid_features = []
    study_area_features = []
    
    summary_stats = []

    for key, info in STUDY_REGIONS.items():
        c_lat = info["center_lat"]
        c_lon = info["center_lon"]
        c_east, c_north = latlon_to_utm43n(c_lat, c_lon)
        
        # Snap center to nearest 5000m to align cleanly with metric coordinates
        half_side = (NUM_CELLS_PER_SIDE * GRID_CELL_SIZE_METERS) / 2.0
        
        min_east = round(c_east - half_side, -3)  # snap to 1000m
        max_east = min_east + (NUM_CELLS_PER_SIDE * GRID_CELL_SIZE_METERS)
        min_north = round(c_north - half_side, -3)
        max_north = min_north + (NUM_CELLS_PER_SIDE * GRID_CELL_SIZE_METERS)
        
        # Calculate WGS84 bounding coordinates
        sw_lat, sw_lon = utm43n_to_latlon(min_east, min_north)
        se_lat, se_lon = utm43n_to_latlon(max_east, min_north)
        ne_lat, ne_lon = utm43n_to_latlon(max_east, max_north)
        nw_lat, nw_lon = utm43n_to_latlon(min_east, max_north)
        
        min_lat = min(sw_lat, se_lat, ne_lat, nw_lat)
        max_lat = max(sw_lat, se_lat, ne_lat, nw_lat)
        min_lon = min(sw_lon, se_lon, ne_lon, nw_lon)
        max_lon = max(sw_lon, se_lon, ne_lon, nw_lon)
        
        boundary_geom = {
            "type": "Polygon",
            "coordinates": [[
                [sw_lon, sw_lat],
                [se_lon, se_lat],
                [ne_lon, ne_lat],
                [nw_lon, nw_lat],
                [sw_lon, sw_lat]
            ]]
        }
        
        boundary_feature = {
            "type": "Feature",
            "properties": {
                "region_id": info["region_id"],
                "region_name": info["region_name"],
                "landscape_type": info["landscape_type"],
                "description": info["description"],
                "scientific_rationale": info["scientific_rationale"],
                "utm_zone": "43N (EPSG:32643)",
                "utm_easting_min": min_east,
                "utm_easting_max": max_east,
                "utm_northing_min": min_north,
                "utm_northing_max": max_north,
                "lat_min": min_lat,
                "lat_max": max_lat,
                "lon_min": min_lon,
                "lon_max": max_lon,
                "grid_cells_x": NUM_CELLS_PER_SIDE,
                "grid_cells_y": NUM_CELLS_PER_SIDE,
                "total_grid_cells": NUM_CELLS_PER_SIDE * NUM_CELLS_PER_SIDE,
                "cell_resolution_km": 5.0,
                "total_area_km2": (NUM_CELLS_PER_SIDE * 5.0)**2
            },
            "geometry": boundary_geom
        }
        study_area_features.append(boundary_feature)
        
        # Save individual study area GeoJSON
        region_geojson = {
            "type": "FeatureCollection",
            "name": f"{info['region_id']}_study_area",
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "features": [boundary_feature]
        }
        with open(os.path.join(output_dir, f"{info['region_id']}_study_area.geojson"), "w") as f:
            json.dump(region_geojson, f, indent=2)
            
        # Generate 10x10 grid cells for this region
        region_grid_features = []
        for r in range(NUM_CELLS_PER_SIDE):
            # Row 0 is southern-most, Row 9 is northern-most
            cell_min_north = min_north + r * GRID_CELL_SIZE_METERS
            cell_max_north = cell_min_north + GRID_CELL_SIZE_METERS
            
            for c in range(NUM_CELLS_PER_SIDE):
                # Col 0 is western-most, Col 9 is eastern-most
                cell_min_east = min_east + c * GRID_CELL_SIZE_METERS
                cell_max_east = cell_min_east + GRID_CELL_SIZE_METERS
                
                c_sw_lat, c_sw_lon = utm43n_to_latlon(cell_min_east, cell_min_north)
                c_se_lat, c_se_lon = utm43n_to_latlon(cell_max_east, cell_min_north)
                c_ne_lat, c_ne_lon = utm43n_to_latlon(cell_max_east, cell_max_north)
                c_nw_lat, c_nw_lon = utm43n_to_latlon(cell_min_east, cell_max_north)
                
                mid_east = (cell_min_east + cell_max_east) / 2.0
                mid_north = (cell_min_north + cell_max_north) / 2.0
                cent_lat, cent_lon = utm43n_to_latlon(mid_east, mid_north)
                
                cell_id = f"{info['prefix']}_R{r+1:02d}_C{c+1:02d}"
                
                cell_feat = {
                    "type": "Feature",
                    "properties": {
                        "cell_id": cell_id,
                        "region_id": info["region_id"],
                        "region_name": info["region_name"],
                        "row_index": r + 1,
                        "col_index": c + 1,
                        "utm_zone": "43N (EPSG:32643)",
                        "utm_min_east": cell_min_east,
                        "utm_max_east": cell_max_east,
                        "utm_min_north": cell_min_north,
                        "utm_max_north": cell_max_north,
                        "centroid_lat": cent_lat,
                        "centroid_lon": cent_lon,
                        "area_km2": 25.0
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [c_sw_lon, c_sw_lat],
                            [c_se_lon, c_se_lat],
                            [c_ne_lon, c_ne_lat],
                            [c_nw_lon, c_nw_lat],
                            [c_sw_lon, c_sw_lat]
                        ]]
                    }
                }
                region_grid_features.append(cell_feat)
                all_grid_features.append(cell_feat)
                
        # Save individual region grid
        with open(os.path.join(output_dir, f"{info['region_id']}_5km_grid.geojson"), "w") as f:
            json.dump({
                "type": "FeatureCollection",
                "name": f"{info['region_id']}_5km_grid",
                "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
                "features": region_grid_features
            }, f, indent=2)
            
        summary_stats.append({
            "region": info["region_name"],
            "lat_range": f"{min_lat:.4f}° N - {max_lat:.4f}° N",
            "lon_range": f"{min_lon:.4f}° E - {max_lon:.4f}° E",
            "utm_easting": f"{min_east:,.0f} - {max_east:,.0f} m",
            "utm_northing": f"{min_north:,.0f} - {max_north:,.0f} m",
            "num_cells": len(region_grid_features),
            "area_km2": (NUM_CELLS_PER_SIDE * 5.0)**2
        })
        
    # Save combined study areas boundary GeoJSON
    with open(os.path.join(output_dir, "study_areas_summary.geojson"), "w") as f:
        json.dump({
            "type": "FeatureCollection",
            "name": "dei_study_areas_summary",
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "features": study_area_features
        }, f, indent=2)
        
    # Save all 300 cells GeoJSON
    with open(os.path.join(output_dir, "all_regions_5km_grid.geojson"), "w") as f:
        json.dump({
            "type": "FeatureCollection",
            "name": "dei_all_regions_5km_grid",
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "features": all_grid_features
        }, f, indent=2)
        
    print("SUCCESS: Generated GeoJSON boundaries and grids.")
    for s in summary_stats:
        print(f"-> {s['region']}: Lat [{s['lat_range']}], Lon [{s['lon_range']}], Cells: {s['num_cells']}, Area: {s['area_km2']} km2")

if __name__ == "__main__":
    out = os.path.abspath("dark_eco/geographical_boundaries")
    generate_spatial_grid_and_boundaries(out)

