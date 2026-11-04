"""
Full GloBI Investigation and Diagnostic Pipeline
Dark Ecology Intelligence (DEI) — Phase 4: GloBI

Retrieves empirical interaction records for the three study windows,
conducts spatial, temporal, taxonomic, and graph audits, and generates
scientific figures and summary metrics.
"""

import json
import logging
import time
from pathlib import Path

import requests
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("globi_investigation")

PROJECT_ROOT = Path("/Users/apple/Documents/5th sem el/ANN_PBL/dark_eco")
CHECKS_DIR = PROJECT_ROOT / "data/metadata/phase_4_checks"
FIGURES_DIR = PROJECT_ROOT / "reports/phase_4/figures"
BOUNDARIES_DIR = PROJECT_ROOT / "geographical_boundaries"

CHECKS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

REGIONS = {
    "bengaluru": {
        "name": "Bengaluru",
        "landscape": "Urban",
        "bbox": "77.3577,12.7396,77.8229,13.1959",
        "poly_file": BOUNDARIES_DIR / "bengaluru_study_area.geojson",
        "grid_file": BOUNDARIES_DIR / "bengaluru_5km_grid.geojson"
    },
    "mysuru": {
        "name": "Mysuru",
        "landscape": "Peri-urban",
        "bbox": "76.4242,12.0790,76.8866,12.5338",
        "poly_file": BOUNDARIES_DIR / "mysuru_study_area.geojson",
        "grid_file": BOUNDARIES_DIR / "mysuru_5km_grid.geojson"
    },
    "nilgiri_bandipur": {
        "name": "Nilgiri-Bandipur",
        "landscape": "Forest",
        "bbox": "76.3658,11.4286,76.8270,11.8832",
        "poly_file": BOUNDARIES_DIR / "nilgiri_bandipur_study_area.geojson",
        "grid_file": BOUNDARIES_DIR / "nilgiri_bandipur_5km_grid.geojson"
    }
}

BASE_URL = "https://api.globalbioticinteractions.org"

def main():
    logger.info("=== Step 1: Querying GloBI API for All Defined Interaction Fields ===")
    field_resp = requests.get(f"{BASE_URL}/interactionFields?type=json", timeout=30)
    field_resp.raise_for_status()
    fields_dict = field_resp.json()
    all_field_names = list(fields_dict.keys())
    logger.info(f"Retrieved {len(all_field_names)} documented GloBI fields.")
    
    # Save field glossary
    field_glossary = [
        {"field": k, "description": v.get("description", "")}
        for k, v in fields_dict.items()
    ]
    pd.DataFrame(field_glossary).to_csv(CHECKS_DIR / "globi_field_glossary.csv", index=False)
    
    fields_param = ",".join(all_field_names)
    
    regional_dfs = {}
    audit_summary = {}
    
    for reg_key, reg_info in REGIONS.items():
        logger.info(f"=== Querying GloBI for {reg_info['name']} ({reg_info['landscape']}) ===")
        params = {
            "bbox": reg_info["bbox"],
            "type": "json",
            "includeObservations": "true",
            "fields": fields_param,
            "limit": 15000
        }
        resp = requests.get(f"{BASE_URL}/interaction", params=params, timeout=60)
        resp.raise_for_status()
        res_json = resp.json()
        
        cols = res_json.get("columns", [])
        rows = res_json.get("data", [])
        df = pd.DataFrame(rows, columns=cols)
        logger.info(f"Retrieved {len(df)} records for {reg_info['name']}.")
        
        # Save raw CSV
        df.to_csv(CHECKS_DIR / f"globi_raw_{reg_key}.csv", index=False)
        
        # Coordinates and geometry
        has_coords = df["latitude"].notnull() & df["longitude"].notnull()
        df_geo = df[has_coords].copy()
        df_geo["lat_float"] = df_geo["latitude"].astype(float)
        df_geo["lon_float"] = df_geo["longitude"].astype(float)
        
        pts = [Point(xy) for xy in zip(df_geo["lon_float"], df_geo["lat_float"])]
        gdf = gpd.GeoDataFrame(df_geo, geometry=pts, crs="EPSG:4326")
        
        # Study polygon containment
        poly_gdf = gpd.read_file(reg_info["poly_file"]).to_crs("EPSG:4326")
        inside_poly = gdf.within(poly_gdf.geometry.iloc[0])
        gdf["inside_study_polygon"] = inside_poly
        
        # 5km Grid assignment
        grid_gdf = gpd.read_file(reg_info["grid_file"]).to_crs("EPSG:4326")
        joined = gpd.sjoin(gdf, grid_gdf[["cell_id", "geometry"]], how="left", predicate="within")
        joined = joined[~joined.index.duplicated(keep="first")]
        
        # Temporal analysis
        dates = pd.to_datetime(joined["event_date"], errors="coerce")
        joined["parsed_year"] = dates.dt.year
        in_2012_2024 = (joined["parsed_year"] >= 2012) & (joined["parsed_year"] <= 2024)
        
        # Taxa
        unique_src_taxa = joined["source_taxon_name"].dropna().unique().tolist()
        unique_tgt_taxa = joined["target_taxon_name"].dropna().unique().tolist()
        all_unique_taxa = list(set(unique_src_taxa) | set(unique_tgt_taxa))
        
        # Studies
        study_counts = joined["study_title"].value_counts().to_dict()
        
        # Top interaction types
        itypes = joined["interaction_type"].value_counts().to_dict()
        
        regional_dfs[reg_key] = joined
        
        audit_summary[reg_key] = {
            "name": reg_info["name"],
            "landscape": reg_info["landscape"],
            "bbox": reg_info["bbox"],
            "total_records_retrieved": len(df),
            "records_with_coordinates": int(has_coords.sum()),
            "records_missing_coordinates": int((~has_coords).sum()),
            "records_inside_polygon": int(inside_poly.sum()),
            "records_outside_polygon": int((~inside_poly).sum()),
            "records_assigned_to_grid": int(joined["cell_id"].notnull().sum()),
            "records_unassigned_grid": int(joined["cell_id"].isnull().sum()),
            "occupied_grid_cells": int(joined["cell_id"].nunique()),
            "total_grid_cells": 100,
            "grid_cell_occupancy_rate": float(joined["cell_id"].nunique()) / 100.0,
            "records_with_date": int(dates.notnull().sum()),
            "records_missing_date": int(dates.isnull().sum()),
            "records_2012_2024": int(in_2012_2024.sum()),
            "records_pre_2012": int((joined["parsed_year"] < 2012).sum()),
            "records_post_2024": int((joined["parsed_year"] > 2024).sum()),
            "unique_source_taxa": len(unique_src_taxa),
            "unique_target_taxa": len(unique_tgt_taxa),
            "unique_total_taxa": len(all_unique_taxa),
            "distinct_studies": len(study_counts),
            "interaction_types": itypes,
            "top_studies": {k[:80]: v for k, v in list(study_counts.items())[:5]}
        }
        
        # Save processed regional GeoJSON/CSV
        joined.drop(columns=["geometry"]).to_csv(CHECKS_DIR / f"globi_audited_{reg_key}.csv", index=False)

    logger.info("=== Step 2: Cross-referencing GloBI Taxa with GBIF Species Inventory ===")
    gbif_species_path = CHECKS_DIR / "gbif_species_summary.csv"
    gbif_df = pd.read_csv(gbif_species_path)
    gbif_species_set = set(gbif_df["species"].dropna())
    
    all_globi_taxa = set()
    regional_overlap = {}
    
    for reg_key, gdf in regional_dfs.items():
        src = set(gdf["source_taxon_name"].dropna())
        tgt = set(gdf["target_taxon_name"].dropna())
        reg_taxa = src | tgt
        all_globi_taxa.update(reg_taxa)
        
        overlap = reg_taxa.intersection(gbif_species_set)
        regional_overlap[reg_key] = {
            "globi_taxa_count": len(reg_taxa),
            "exact_binomial_overlap_count": len(overlap),
            "overlap_percentage": float(len(overlap)) / len(reg_taxa) * 100.0 if reg_taxa else 0.0,
            "sample_overlapping_species": sorted(list(overlap))[:10]
        }
    
    total_globi_overlap = all_globi_taxa.intersection(gbif_species_set)
    overlap_summary = {
        "total_gbif_species": len(gbif_species_set),
        "total_unique_globi_taxa": len(all_globi_taxa),
        "total_exact_binomial_matches": len(total_globi_overlap),
        "total_overlap_percentage": float(len(total_globi_overlap)) / len(all_globi_taxa) * 100.0,
        "regional_breakdown": regional_overlap
    }
    
    # Save complete JSON summary
    complete_summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_url": BASE_URL,
        "study_landscapes": audit_summary,
        "taxonomic_overlap_with_gbif": overlap_summary
    }
    with open(CHECKS_DIR / "globi_investigation_summary.json", "w", encoding="utf-8") as f:
        json.dump(complete_summary, f, indent=2)
    logger.info("Saved globi_investigation_summary.json.")

    logger.info("=== Step 3: Generating Publication Figures (300 DPI) ===")
    
    # Figure 1: Record counts by region & temporal window
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    names = [r["name"] for r in audit_summary.values()]
    retrieved = [r["total_records_retrieved"] for r in audit_summary.values()]
    inside_poly = [r["records_inside_polygon"] for r in audit_summary.values()]
    window_2012_2024 = [r["records_2012_2024"] for r in audit_summary.values()]
    
    x = np.arange(len(names))
    width = 0.25
    
    ax.bar(x - width, retrieved, width, label="Retrieved from Bounding Box", color="#1f77b4")
    ax.bar(x, inside_poly, width, label="Inside Study Polygon", color="#2ca02c")
    ax.bar(x + width, window_2012_2024, width, label="Aligned 2012–2024 Window", color="#ff7f0e")
    
    ax.set_ylabel("Number of Empirical Interaction Records", fontsize=12, fontweight="bold")
    ax.set_title("GloBI Regional Interaction Records Across Study Windows", fontsize=14, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=11, fontweight="bold")
    ax.legend(frameon=True, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    
    for i in range(len(names)):
        ax.text(x[i] - width, retrieved[i] + 100, f"{retrieved[i]:,}", ha="center", fontsize=9)
        ax.text(x[i], inside_poly[i] + 100, f"{inside_poly[i]:,}", ha="center", fontsize=9)
        ax.text(x[i] + width, window_2012_2024[i] + 100, f"{window_2012_2024[i]:,}", ha="center", fontsize=9)
        
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "globi_records_by_region.png", dpi=300)
    plt.close()
    
    # Figure 2: Top Interaction Types Breakdown
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=300, sharey=False)
    for ax, (reg_key, reg_info) in zip(axes, REGIONS.items()):
        itypes = audit_summary[reg_key]["interaction_types"]
        top_types = pd.Series(itypes).head(6)
        y_pos = np.arange(len(top_types))
        ax.barh(y_pos, top_types.values, color="#3470a3", edgecolor="black", linewidth=0.8)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_types.index, fontsize=10, fontweight="bold")
        ax.invert_yaxis()
        ax.set_xlabel("Record Count", fontsize=10)
        ax.set_title(f"{reg_info['name']} ({reg_info['landscape']})", fontsize=12, fontweight="bold")
        ax.grid(axis="x", linestyle="--", alpha=0.5)
        for i, v in enumerate(top_types.values):
            ax.text(v + 10, i, f"{v:,}", va="center", fontsize=9)
            
    fig.suptitle("GloBI Documented Biotic Interaction Types Across Study Windows", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "globi_interaction_types_breakdown.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Figure 3: Temporal Distribution
    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    all_years = []
    labels = []
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for reg_key, gdf in regional_dfs.items():
        all_years.append(gdf["parsed_year"].dropna())
        labels.append(audit_summary[reg_key]["name"])
        
    bins = np.arange(1990, 2028, 1)
    ax.hist(all_years, bins=bins, stacked=True, label=labels, color=colors, edgecolor="black", alpha=0.85)
    ax.axvspan(2012, 2024.9, color="yellow", alpha=0.2, label="Approved 2012–2024 Study Window")
    ax.set_xlabel("Observation Event Year", fontsize=12, fontweight="bold")
    ax.set_ylabel("Number of Interaction Records", fontsize=12, fontweight="bold")
    ax.set_title("Temporal Distribution of Empirical GloBI Interactions (1990–2026)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlim(1990, 2027)
    ax.legend(frameon=True, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "globi_temporal_distribution.png", dpi=300)
    plt.close()

    # Figure 4: Spatial Cell Occupancy (Grid Level)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=300)
    for ax, (reg_key, reg_info) in zip(axes, REGIONS.items()):
        gdf = regional_dfs[reg_key]
        cell_counts = gdf["cell_id"].value_counts()
        occupied = len(cell_counts)
        empty = 100 - occupied
        
        ax.bar(["Occupied Cells\n(>=1 Interaction)", "Zero-Interaction\nCells"], [occupied, empty],
               color=["#2ca02c", "#d62728"], edgecolor="black", width=0.5)
        ax.set_ylabel("Number of 5km Grid Cells", fontsize=10)
        ax.set_ylim(0, 110)
        ax.set_title(f"{reg_info['name']} ({occupied}/100 Cells Occupied)", fontsize=11, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.text(0, occupied + 3, f"{occupied}%", ha="center", fontweight="bold")
        ax.text(1, empty + 3, f"{empty}%", ha="center", fontweight="bold")
        
    fig.suptitle("Spatial Grid-Cell Coverage of GloBI Interactions Across 100-Cell Grids", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "globi_spatial_cell_occupancy.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Figure 5: Taxonomic Overlap between GloBI and GBIF
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    
    # Bar plot of overlap
    reg_names = [r["name"] for r in audit_summary.values()]
    globi_taxa_counts = [regional_overlap[k]["globi_taxa_count"] for k in regional_overlap]
    matched_counts = [regional_overlap[k]["exact_binomial_overlap_count"] for k in regional_overlap]
    
    x = np.arange(len(reg_names))
    width = 0.35
    ax1.bar(x - width/2, globi_taxa_counts, width, label="Unique GloBI Taxa", color="#4a7bb0", edgecolor="black")
    ax1.bar(x + width/2, matched_counts, width, label="GBIF Binomial Match", color="#59a14f", edgecolor="black")
    ax1.set_xticks(x)
    ax1.set_xticklabels(reg_names, fontweight="bold")
    ax1.set_ylabel("Number of Taxa", fontsize=11, fontweight="bold")
    ax1.set_title("Taxonomic Overlap per Landscape", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    for i in range(len(reg_names)):
        pct = regional_overlap[list(regional_overlap.keys())[i]]["overlap_percentage"]
        ax1.text(x[i] + width/2, matched_counts[i] + 15, f"{pct:.1f}%", ha="center", fontsize=9, fontweight="bold")

    # Overall dataset pie chart
    match_total = len(total_globi_overlap)
    unmatched_total = len(all_globi_taxa) - match_total
    ax2.pie([match_total, unmatched_total], labels=[f"Exact GBIF Match\n({match_total:,} species)", f"GloBI Taxa Not in GBIF\n({unmatched_total:,} taxa)"],
            autopct="%1.1f%%", startangle=140, colors=["#59a14f", "#e15759"],
            explode=(0.05, 0), textprops={"fontsize": 10, "fontweight": "bold"})
    ax2.set_title(f"Overall Taxa Overlap (Total Unique GloBI Taxa = {len(all_globi_taxa):,})", fontsize=12, fontweight="bold")

    plt.suptitle("GloBI Interactions vs. GBIF DWCA Occurrence Taxonomic Inventory", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "globi_gbif_taxonomic_overlap.png", dpi=300, bbox_inches="tight")
    plt.close()

    logger.info("=== All figures generated and saved successfully in reports/phase_4/figures/ ===")

if __name__ == "__main__":
    main()

