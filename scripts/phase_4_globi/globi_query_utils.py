"""
GloBI Query and Analysis Utilities for Dark Ecology Intelligence (DEI)
Phase 4: Global Biotic Interactions Investigation

Provides robust query methods, coordinate validation, spatial joining with
study polygons and 5km grid cells, and taxonomic overlap analysis with GBIF.
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("globi_utils")

GLOBI_BASE_URL = "https://api.globalbioticinteractions.org"

# Approved bounding boxes for the 3 study regions
STUDY_BBOXES = {
    "bengaluru": "77.3577,12.7396,77.8229,13.1959",
    "mysuru": "76.4242,12.0790,76.8866,12.5338",
    "nilgiri_bandipur": "76.3658,11.4286,76.8270,11.8832"
}

def get_interaction_fields() -> Dict[str, Any]:
    """Retrieve all defined interaction fields and descriptions from GloBI."""
    url = f"{GLOBI_BASE_URL}/interactionFields?type=json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

def query_globi_bbox(
    bbox: str,
    include_observations: bool = True,
    fields: Optional[List[str]] = None,
    limit: int = 15000,
    offset: int = 0
) -> pd.DataFrame:
    """
    Query GloBI API for interactions within a bounding box.
    
    Args:
        bbox: "minLon,minLat,maxLon,maxLat" in EPSG:4326.
        include_observations: If True, retrieves empirical observation records with lat/lon.
        fields: Optional list of field names. If None, requests all defined fields.
        limit: Maximum records to return.
        offset: Offset for pagination.
    
    Returns:
        pd.DataFrame containing the interaction records.
    """
    url = f"{GLOBI_BASE_URL}/interaction"
    params = {
        "bbox": bbox,
        "type": "json",
        "limit": limit,
        "offset": offset
    }
    if include_observations:
        params["includeObservations"] = "true"
        
    if fields:
        params["fields"] = ",".join(fields)
    else:
        # Get all field names
        field_dict = get_interaction_fields()
        params["fields"] = ",".join(list(field_dict.keys()))

    logger.info(f"Querying GloBI: bbox={bbox}, limit={limit}, offset={offset}")
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    res_json = resp.json()
    
    cols = res_json.get("columns", [])
    rows = res_json.get("data", [])
    df = pd.DataFrame(rows, columns=cols)
    logger.info(f"Received {len(df)} rows ({len(cols)} columns)")
    return df

def spatial_audit_region(
    df: pd.DataFrame,
    polygon_path: str,
    grid_path: str
) -> Tuple[gpd.GeoDataFrame, Dict[str, Any]]:
    """
    Audit spatial coordinates against study polygon and 5km grid cells.
    
    Returns:
        GeoDataFrame with spatial assignment and audit metrics dictionary.
    """
    metrics = {
        "total_records": len(df),
        "has_coordinates": 0,
        "missing_coordinates": 0,
        "inside_study_polygon": 0,
        "outside_study_polygon": 0,
        "assigned_to_grid_cells": 0,
        "unassigned_grid_cells": 0,
        "occupied_cell_count": 0,
        "total_cells": 100
    }
    
    if df.empty:
        return gpd.GeoDataFrame(), metrics
        
    has_lat_lon = df["latitude"].notnull() & df["longitude"].notnull()
    metrics["has_coordinates"] = int(has_lat_lon.sum())
    metrics["missing_coordinates"] = int((~has_lat_lon).sum())
    
    df_valid = df[has_lat_lon].copy()
    df_valid["lat_float"] = df_valid["latitude"].astype(float)
    df_valid["lon_float"] = df_valid["longitude"].astype(float)
    
    pts = [Point(xy) for xy in zip(df_valid["lon_float"], df_valid["lat_float"])]
    gdf = gpd.GeoDataFrame(df_valid, geometry=pts, crs="EPSG:4326")
    
    # Study polygon containment
    poly_gdf = gpd.read_file(polygon_path)
    if poly_gdf.crs != "EPSG:4326":
        poly_gdf = poly_gdf.to_crs("EPSG:4326")
    poly_geom = poly_gdf.geometry.iloc[0]
    
    inside_mask = gdf.within(poly_geom)
    metrics["inside_study_polygon"] = int(inside_mask.sum())
    metrics["outside_study_polygon"] = int((~inside_mask).sum())
    gdf["inside_study_polygon"] = inside_mask
    
    # 5km Grid assignment
    grid_gdf = gpd.read_file(grid_path)
    if grid_gdf.crs != "EPSG:4326":
        grid_gdf = grid_gdf.to_crs("EPSG:4326")
        
    joined = gpd.sjoin(gdf, grid_gdf[["cell_id", "geometry"]], how="left", predicate="within")
    # Clean duplicates from boundary touching if any
    joined = joined[~joined.index.duplicated(keep="first")]
    
    assigned_mask = joined["cell_id"].notnull()
    metrics["assigned_to_grid_cells"] = int(assigned_mask.sum())
    metrics["unassigned_grid_cells"] = int((~assigned_mask).sum())
    metrics["occupied_cell_count"] = int(joined["cell_id"].nunique())
    
    return joined, metrics

