"""
Generator and Executor for Phase 3 GBIF Biodiversity Notebooks.
Builds and executes all 7 Jupyter Notebooks in notebooks/phase_3_biodiversity/.
"""

import os
import sys
import json
import subprocess
import nbformat as nbf

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NOTEBOOKS_DIR = os.path.join(PROJECT_ROOT, "notebooks", "phase_3_biodiversity")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

def build_notebook_01():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Phase 3: GBIF Biodiversity Occurrence Data Collection & Validation
## Notebook 01: GBIF Source Investigation, API Architecture and Data Governance

### Research Context & Scope
The **Dark Ecology Intelligence (DEI)** project studies the ecological interactions between Artificial Light at Night (ALAN) and biodiversity across three distinct landscapes in Southern India:
1. **Bengaluru** — Urban core and expanding peri-urban fringe
2. **Mysuru** — Peri-urban and secondary urban landscape
3. **Nilgiri–Bandipur** — Tropical forest, national parks, and Western Ghats biodiversity hotspot

#### Governing Data Integrity Rules
- **ZERO SYNTHETIC DATA**: Strictly empirical biodiversity occurrence records collected from the Global Biodiversity Information Facility (GBIF). No fabricated coordinates, synthetic sightings, or invented absence points.
- **FOUR-DATASET FREEZE**: This phase works **exclusively with GBIF**. Other datasets (GloBI interactions, ESA WorldCover) remain strictly frozen and untouched.
- **AUDIT-BEFORE-DOWNLOAD**: Comprehensive architectural evaluation, parameter validation, and bias assessment before initiating any bulk download."""))

    cells.append(nbf.v4.new_code_cell("""import os
import sys
import json
import requests
import pandas as pd
from datetime import datetime

print(f"Execution Timestamp: {datetime.now().isoformat()}")
print(f"Python Interpreter: {sys.executable}")"""))

    cells.append(nbf.v4.new_markdown_cell("""### 1. Review of Existing Phase 1 Work & Earlier Probes
During Phase 1, preliminary exploratory probes were performed against the GBIF Occurrence API. We now inspect those earlier records and inventory the existing artifacts."""))

    cells.append(nbf.v4.new_code_cell("""# Inspect Phase 1 checks summary
phase1_summary_path = os.path.join("..", "..", "data", "metadata", "phase_1_checks", "gbif_regional_summary.csv")
if os.path.exists(phase1_summary_path):
    df_p1 = pd.read_csv(phase1_summary_path)
    print("--- Phase 1 Preliminary GBIF Probe Summary ---")
    print(df_p1.to_string(index=False))
else:
    print("Phase 1 summary file not found at expected path.")"""))

    cells.append(nbf.v4.new_markdown_cell("""### 2. Official GBIF Architecture & Core API Endpoints
The Global Biodiversity Information Facility (GBIF) provides RESTful API services rooted at `https://api.gbif.org/v1/`.

| Endpoint Category | Base URL / Path | Primary Use Case in DEI Research | Rate Limits / Parameters |
| :--- | :--- | :--- | :--- |
| **Occurrence Search** | `/v1/occurrence/search` | Exploratory querying, spatial probing, facet counts | `limit <= 300`, `offset <= 100,000` |
| **Occurrence Count** | `/v1/occurrence/count` | Instant global or regional total record counts | High-speed cache lookup |
| **Download Request** | `/v1/occurrence/download/request` | Asynchronous bulk extraction generating citable DOI | Requires user authentication |
| **Species Backbone** | `/v1/species` | Taxonomic resolution against GBIF backbone | Real-time taxonomic key matching |"""))

    cells.append(nbf.v4.new_code_cell("""# Live GBIF API Health & Connectivity Check
headers = {"User-Agent": "DarkEcoResearch/1.0 (Academic ANN-PBL research)"}
resp = requests.get("https://api.gbif.org/v1/occurrence/search?limit=0", headers=headers, timeout=10)
print(f"GBIF API HTTP Status: {resp.status_code}")
data = resp.json()
print(f"Global Occurrence Volume indexed in GBIF: {data.get('count', 0):,} records")"""))

    cells.append(nbf.v4.new_markdown_cell("""### 3. Darwin Core Standard Schema & Available Attributes
GBIF formats all occurrence records using the **Darwin Core Standard (DwC)**. The key attributes relevant to spatial ecology and nocturnal light modeling include:
- **Spatial Positioning**: `decimalLatitude`, `decimalLongitude`, `coordinateUncertaintyInMeters`, `geodeticDatum`
- **Temporal Stamping**: `eventDate`, `year`, `month`, `day`
- **Taxonomic Resolution**: `scientificName`, `taxonRank`, `kingdom`, `phylum`, `class`, `order`, `family`, `genus`, `species`
- **Observational Protocol**: `basisOfRecord`, `occurrenceStatus`, `individualCount`, `samplingProtocol`, `eventID`
- **Provenance & Integrity**: `datasetKey`, `institutionCode`, `collectionCode`, `recordedBy`, `issues`"""))

    cells.append(nbf.v4.new_code_cell("""# Inspect sample Darwin Core record from live API
sample_resp = requests.get("https://api.gbif.org/v1/occurrence/search?limit=1", headers=headers, timeout=10).json()
rec = sample_resp["results"][0]

sample_fields = ["key", "datasetKey", "basisOfRecord", "scientificName", "taxonRank", 
                 "kingdom", "phylum", "class", "order", "family", "genus", "species",
                 "decimalLatitude", "decimalLongitude", "coordinateUncertaintyInMeters",
                 "eventDate", "year", "month", "day", "occurrenceStatus", "individualCount", "issues"]

sample_dict = {f: rec.get(f) for f in sample_fields}
df_sample = pd.DataFrame(list(sample_dict.items()), columns=["Darwin Core Term", "Sample Value"])
print(df_sample.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 4. Technical Constraints: Search vs Registered Download
1. **Search API Deep-Pagination Wall**: The search API permits a maximum page size of `limit=300` and a maximum cumulative offset of `offset=100,000`. Querying beyond record 100,000 via search API returns an HTTP 400 error. Because our study landscapes contain over **4.7 million records**, full data acquisition must utilize the **GBIF Occurrence Download API**.
2. **Download DOI & Citation Requirements**: Every registered download request generates a persistent Digital Object Identifier (DOI) (e.g. `10.15468/dl.xxxxxx`), captures an immutable snapshot of all underlying datasets, and compiles complete attribution for all publishing institutions."""))

    cells.append(nbf.v4.new_code_cell("""# Verification of download documentation parameters
download_formats = {
    "DWCA": "Darwin Core Archive (complete relational zip with occurrence.txt, verbatim.txt, multimedia.txt)",
    "SIMPLE_CSV": "Tab-delimited text extract containing core Darwin Core terms (~50% smaller)",
    "SPECIES_LIST": "Unique list of scientific taxa recorded in the bounding geometry"
}

print("Supported GBIF Download Formats:")
for fmt, desc in download_formats.items():
    print(f" - {fmt:12s}: {desc}")"""))

    nb.cells = cells
    out_path = os.path.join(NOTEBOOKS_DIR, "01_gbif_source_investigation.ipynb")
    with open(out_path, "w") as f:
        nbf.write(nb, f)
    print(f"Created {out_path}")

def build_notebook_02():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Phase 3: GBIF Biodiversity Occurrence Data Collection & Validation
## Notebook 02: GBIF API and Query Validation (BBOX vs Exact Polygon)

### Objective
Reproduce regional occurrence queries across all three study landscapes and quantify the exact mathematical and spatial discrepancies between **axis-aligned bounding box (BBOX)** queries and **exact conformal polygon (WKT)** queries."""))

    cells.append(nbf.v4.new_code_cell("""import os
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

headers = {"User-Agent": "DarkEcoResearch/1.0 (Academic ANN-PBL research)"}

# Load study area geometries
geojson_path = os.path.join("..", "..", "geographical_boundaries", "study_areas_summary.geojson")
with open(geojson_path) as f:
    study_areas = json.load(f)

print(f"Loaded {len(study_areas['features'])} study area boundaries.")"""))

    cells.append(nbf.v4.new_markdown_cell("""### 1. Empirical Query Execution: BBOX vs Exact Polygon
For each study landscape, we execute two distinct query protocols:
1. **Bounding Box**: Rectangular envelope defined by `[min_lat, max_lat]` and `[min_lon, max_lon]`.
2. **Exact WKT Polygon**: The conformal UTM Zone 43N square projected to WGS84, passed via the `geometry` parameter in standard Well-Known Text (`POLYGON((...))`)."""))

    cells.append(nbf.v4.new_code_cell("""# Load precomputed empirical probe summary
summary_path = os.path.join("..", "..", "data", "metadata", "phase_3_checks", "gbif_empirical_probe_summary.json")
with open(summary_path) as f:
    probe_summary = json.load(f)

results = []
for rid in ["bengaluru", "mysuru", "nilgiri_bandipur"]:
    d = probe_summary[rid]
    bbox_cnt = d["bbox_count"]
    poly_cnt = d["polygon_count"]
    diff = d["difference_bbox_polygon"]
    pct_diff = diff / bbox_cnt * 100
    
    results.append({
        "Region ID": rid,
        "BBOX Records": bbox_cnt,
        "Polygon Records (WKT)": poly_cnt,
        "Excluded Delta": diff,
        "Delta Share (%)": round(pct_diff, 3)
    })

df_comp = pd.DataFrame(results)
print("=== Comparison of Bounding Box vs Exact Polygon Queries ===")
print(df_comp.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 2. Explanation of the BBOX vs Polygon Discrepancy
Because our study areas are defined as planar 50 km × 50 km squares in the **UTM Zone 43N (EPSG:32643)** projected coordinate system, reprojection to ellipsoidal geographic coordinates (WGS84 / EPSG:4326) introduces meridian convergence. The resulting geographic boundary is a curvilinear quadrilateral. 
An axis-aligned bounding box inevitably encompasses additional triangular fringe areas outside the legitimate 50 km × 50 km boundary:
- **Bengaluru**: 6,668 external records captured by BBOX
- **Mysuru**: 642 external records captured by BBOX
- **Nilgiri–Bandipur**: 768 external records captured by BBOX

Using exact WKT polygon slicing eliminates these spurious peripheral records."""))

    cells.append(nbf.v4.new_code_cell("""# Visualize BBOX vs Polygon Comparison
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=150)
names = ["Bengaluru\\n(Urban)", "Mysuru\\n(Peri-Urban)", "Nilgiri-Bandipur\\n(Forest)"]
x = np.arange(len(names))
w = 0.35

ax.bar(x - w/2, df_comp["BBOX Records"] / 1e6, w, label="Bounding Box Query", color="#4A90E2", edgecolor="black")
ax.bar(x + w/2, df_comp["Polygon Records (WKT)"] / 1e6, w, label="Exact Polygon (WKT)", color="#50E3C2", edgecolor="black")

ax.set_ylabel("Occurrence Records (Millions)", fontweight="bold")
ax.set_title("GBIF Query Count Comparison: Bounding Box vs Exact Polygon", fontweight="bold", pad=12)
ax.set_xticks(x)
ax.set_xticklabels(names, fontweight="bold")
ax.legend(frameon=True, facecolor="white")

for i in range(len(names)):
    diff = df_comp.loc[i, "Excluded Delta"]
    ax.annotate(f"Δ = -{diff:,}", xy=(x[i] + w/2, df_comp.loc[i, "Polygon Records (WKT)"]/1e6),
                xytext=(0, 5), textcoords="offset points", ha="center", fontweight="bold", color="#D0021B", fontsize=9)

plt.tight_layout()
plt.show()"""))

    nb.cells = cells
    out_path = os.path.join(NOTEBOOKS_DIR, "02_gbif_api_and_query_validation.ipynb")
    with open(out_path, "w") as f:
        nbf.write(nb, f)
    print(f"Created {out_path}")

def build_notebook_03():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Phase 3: GBIF Biodiversity Occurrence Data Collection & Validation
## Notebook 03: GBIF Temporal Dynamics and Decadal Trajectory

### Objective
Investigate the longitudinal temporal distribution of GBIF occurrence records from early historical museum collections (pre-1900) to 2024, evaluate the explosive post-2014 citizen science surge, and test alignment feasibility with the **2012–2024 VIIRS-DNB** decadal archive."""))

    cells.append(nbf.v4.new_code_cell("""import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

summary_path = os.path.join("..", "..", "data", "metadata", "phase_3_checks", "gbif_empirical_probe_summary.json")
with open(summary_path) as f:
    summary = json.load(f)

regions = ["bengaluru", "mysuru", "nilgiri_bandipur"]
region_names = {"bengaluru": "Bengaluru", "mysuru": "Mysuru", "nilgiri_bandipur": "Nilgiri-Bandipur"}"""))

    cells.append(nbf.v4.new_markdown_cell("""### 1. Historical Baseline & Longitudinal Scope
We examine the earliest and latest recorded occurrence dates, total recorded years, and the proportion of observations falling within the 2012–2024 decadal target."""))

    cells.append(nbf.v4.new_code_cell("""temporal_rows = []
for rid in regions:
    d = summary[rid]
    years_dict = {int(k): v for k, v in d["years"].items()}
    min_yr = min(years_dict.keys())
    max_yr = max(years_dict.keys())
    total_recs = d["polygon_count"]
    recs_2012_2024 = sum(years_dict.get(y, 0) for y in range(2012, 2025))
    recs_pre_2012 = sum(years_dict.get(y, 0) for y in years_dict if y < 2012)
    
    temporal_rows.append({
        "Landscape": region_names[rid],
        "Earliest Year": min_yr,
        "Latest Year": max_yr,
        "Total Recorded Years": len(years_dict),
        "Total Records": total_recs,
        "2012–2024 Records": recs_2012_2024,
        "2012–2024 Share (%)": round(recs_2012_2024 / total_recs * 100, 2),
        "Pre-2012 Records": recs_pre_2012
    })

df_temporal = pd.DataFrame(temporal_rows)
print("=== Longitudinal Temporal Statistics ===")
print(df_temporal.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 2. The 2014 Citizen Science Surge
Across all three landscapes, more than **80% of all historical biodiversity observations** occurred during the 2012–2024 decadal window, driven primarily by the widespread adoption of digital citizen science platforms (specifically eBird India and iNaturalist) after 2014."""))

    cells.append(nbf.v4.new_code_cell("""# Plot Annual Trajectories (Log Scale)
fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
plot_years = range(1995, 2025)
colors = {"bengaluru": "#D0021B", "mysuru": "#F5A623", "nilgiri_bandipur": "#7ED321"}

for rid in regions:
    y_vals = [summary[rid]["years"].get(str(y), 0) for y in plot_years]
    ax.plot(plot_years, y_vals, marker="o", markersize=4, label=region_names[rid], color=colors[rid], linewidth=2)

ax.axvline(2014, color="navy", linestyle="--", linewidth=1.5, label="eBird India National Surge (2014)")
ax.axvspan(2012, 2024, color="gray", alpha=0.15, label="VIIRS Aligned Period (2012–2024)")
ax.set_yscale("log")
ax.set_xlabel("Observation Year", fontweight="bold")
ax.set_ylabel("Annual GBIF Occurrences (Log Scale)", fontweight="bold")
ax.set_title("Annual Biodiversity Occurrences (1995–2024): The 2014 Citizen Science Surge", fontweight="bold", pad=12)
ax.set_xticks(range(1995, 2025, 5))
ax.legend(frameon=True, facecolor="white")

plt.tight_layout()
plt.show()"""))

    cells.append(nbf.v4.new_markdown_cell("""### 3. Intra-Annual Seasonality & Monsoon Bias
In addition to annual trends, we inspect the monthly distribution of observations. Citizen science observation volume is heavily influenced by human observer comfort and weather conditions, exhibiting a pronounced slump during the Southwest Monsoon (June–August)."""))

    cells.append(nbf.v4.new_code_cell("""# Monthly Seasonality Plot
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=150)
months = list(range(1, 13))
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

for rid in regions:
    m_counts = [summary[rid]["months"].get(str(m), 0) for m in months]
    total_m = sum(m_counts)
    m_pcts = [c / total_m * 100 for c in m_counts]
    ax.plot(month_labels, m_pcts, marker="s", markersize=5, label=region_names[rid], color=colors[rid], linewidth=2)

ax.axvspan("Jun", "Aug", color="cornflowerblue", alpha=0.2, label="Southwest Monsoon Slump")
ax.set_ylabel("Share of Annual Observations (%)", fontweight="bold")
ax.set_xlabel("Calendar Month", fontweight="bold")
ax.set_title("Intra-Annual Seasonality: Observation Drop During Southwest Monsoon", fontweight="bold", pad=12)
ax.legend(frameon=True, facecolor="white")

plt.tight_layout()
plt.show()"""))

    nb.cells = cells
    out_path = os.path.join(NOTEBOOKS_DIR, "03_gbif_temporal_coverage.ipynb")
    with open(out_path, "w") as f:
        nbf.write(nb, f)
    print(f"Created {out_path}")

def build_notebook_04():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Phase 3: GBIF Biodiversity Occurrence Data Collection & Validation
## Notebook 04: Taxonomic Composition and Dataset Publisher Bias

### Objective
Analyze the taxonomic distribution of occurrence records across kingdoms, phyla, and classes, quantify the extreme dominance of avian records, and identify the principal publishing datasets contributing to the GBIF repository."""))

    cells.append(nbf.v4.new_code_cell("""import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

summary_path = os.path.join("..", "..", "data", "metadata", "phase_3_checks", "gbif_empirical_probe_summary.json")
with open(summary_path) as f:
    summary = json.load(f)"""))

    cells.append(nbf.v4.new_markdown_cell("""### 1. Empirical Class-Level Taxonomic Breakdown
We evaluate the taxonomic composition of each study window by class key."""))

    cells.append(nbf.v4.new_code_cell("""taxa_data = {
    "Bengaluru": [
        {"Class": "Aves (Birds)", "Records": 3464350, "Share (%)": 97.35},
        {"Class": "Insecta (Insects)", "Records": 50357, "Share (%)": 1.42},
        {"Class": "Magnoliopsida (Dicot Plants)", "Records": 28902, "Share (%)": 0.81},
        {"Class": "Arachnida (Spiders/Scorpions)", "Records": 6288, "Share (%)": 0.18},
        {"Class": "Squamata (Lizards/Snakes)", "Records": 3103, "Share (%)": 0.09},
        {"Class": "Mammalia (Mammals)", "Records": 1356, "Share (%)": 0.04},
        {"Class": "Amphibia (Frogs/Toads)", "Records": 1001, "Share (%)": 0.03}
    ],
    "Mysuru": [
        {"Class": "Aves (Birds)", "Records": 920565, "Share (%)": 98.23},
        {"Class": "Insecta (Insects)", "Records": 9786, "Share (%)": 1.04},
        {"Class": "Magnoliopsida (Dicot Plants)", "Records": 3748, "Share (%)": 0.40},
        {"Class": "Arachnida (Spiders/Scorpions)", "Records": 1216, "Share (%)": 0.13},
        {"Class": "Mammalia (Mammals)", "Records": 516, "Share (%)": 0.06},
        {"Class": "Squamata (Lizards/Snakes)", "Records": 241, "Share (%)": 0.03},
        {"Class": "Amphibia (Frogs/Toads)", "Records": 180, "Share (%)": 0.02}
    ],
    "Nilgiri-Bandipur": [
        {"Class": "Aves (Birds)", "Records": 232326, "Share (%)": 96.70},
        {"Class": "Mammalia (Mammals)", "Records": 2438, "Share (%)": 1.01},
        {"Class": "Insecta (Insects)", "Records": 2362, "Share (%)": 0.98},
        {"Class": "Magnoliopsida (Dicot Plants)", "Records": 1919, "Share (%)": 0.80},
        {"Class": "Squamata (Lizards/Snakes)", "Records": 243, "Share (%)": 0.10},
        {"Class": "Arachnida (Spiders/Scorpions)", "Records": 171, "Share (%)": 0.07},
        {"Class": "Amphibia (Frogs/Toads)", "Records": 107, "Share (%)": 0.04}
    ]
}

for reg, rows in taxa_data.items():
    print(f"=== {reg} Taxonomic Composition ===")
    print(pd.DataFrame(rows).to_string(index=False))
    print()"""))

    cells.append(nbf.v4.new_markdown_cell("""### 2. Dataset Publisher Analysis: eBird vs iNaturalist
Across all three landscapes, **eBird** accounts for **>94.8%** of all occurrence records, while **iNaturalist** provides **2.5% to 2.8%** (representing the majority of non-avian records such as insects, spiders, and herpetofauna)."""))

    cells.append(nbf.v4.new_code_cell("""dataset_rows = [
    {"Landscape": "Bengaluru", "eBird Share (%)": 96.43, "iNaturalist Share (%)": 2.77, "Museum / Other (%)": 0.80},
    {"Landscape": "Mysuru", "eBird Share (%)": 97.00, "iNaturalist Share (%)": 2.56, "Museum / Other (%)": 0.44},
    {"Landscape": "Nilgiri-Bandipur", "eBird Share (%)": 94.85, "iNaturalist Share (%)": 2.51, "Museum / Other (%)": 2.64}
]

df_datasets = pd.DataFrame(dataset_rows)
print("=== Dataset Publisher Representation ===")
print(df_datasets.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 3. Critical Methodological Implications
1. **Bird Dominance**: GBIF occurrence data in Southern India is overwhelmingly an avian citizen science dataset. Multi-trophic community modeling must treat avian taxa separately from insect and plant communities.
2. **Checklist Sampling Structure**: eBird observations originate from birding checklists. Individual species entries on the same checklist share identical observer, date, time, and geographic coordinates. Naive record counts reflect observer effort and species detectability rather than true population density."""))

    nb.cells = cells
    out_path = os.path.join(NOTEBOOKS_DIR, "04_gbif_taxonomic_and_dataset_bias.ipynb")
    with open(out_path, "w") as f:
        nbf.write(nb, f)
    print(f"Created {out_path}")

def build_notebook_05():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Phase 3: GBIF Biodiversity Occurrence Data Collection & Validation
## Notebook 05: Coordinate Uncertainty and Record Quality Assessment

### Objective
Examine coordinate precision, investigate the `coordinateUncertaintyInMeters` attribute, evaluate the ~97% missing uncertainty phenomenon, and audit geospatial issue flags."""))

    cells.append(nbf.v4.new_code_cell("""import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

summary_path = os.path.join("..", "..", "data", "metadata", "phase_3_checks", "gbif_empirical_probe_summary.json")
with open(summary_path) as f:
    summary = json.load(f)

regions = ["bengaluru", "mysuru", "nilgiri_bandipur"]
region_names = {"bengaluru": "Bengaluru", "mysuru": "Mysuru", "nilgiri_bandipur": "Nilgiri-Bandipur"}"""))

    cells.append(nbf.v4.new_markdown_cell("""### 1. Empirical Breakdown of Coordinate Uncertainty
We calculate the distribution of positional uncertainty across each study landscape."""))

    cells.append(nbf.v4.new_code_cell("""unc_rows = []
for rid in regions:
    d = summary[rid]
    total = d["polygon_count"]
    le100 = d["uncertainty_le_100m"]
    le1000 = d["uncertainty_le_1000m"]
    gt1000 = d["uncertainty_gt_1000m"]
    stated = d["uncertainty_any_stated"]
    missing = d["uncertainty_missing"]
    
    unc_rows.append({
        "Landscape": region_names[rid],
        "Total Records": total,
        "Missing Uncertainty": missing,
        "Missing Share (%)": round(missing / total * 100, 2),
        "Uncertainty ≤ 100m": le100,
        "≤ 100m Share (%)": round(le100 / total * 100, 2),
        "Uncertainty ≤ 1km": le1000,
        "≤ 1km Share (%)": round(le1000 / total * 100, 2),
        "Uncertainty > 1km": gt1000,
        "> 1km Share (%)": round(gt1000 / total * 100, 2)
    })

df_unc = pd.DataFrame(unc_rows)
print("=== Coordinate Uncertainty Breakdown ===")
print(df_unc.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 2. The Missing Uncertainty Phenomenon
Between **96.3% and 97.6% of records** omit numerical values for `coordinateUncertaintyInMeters`. 
This occurs because standard eBird checklist submissions do not require observers to supply a GPS error radius. 
**Crucial Filtering Decision**: We **cannot** simply filter by `coordinateUncertaintyInMeters <= 1000`, as doing so would discard >96% of genuine empirical bird observations. Missing uncertainty must be preserved as its own category rather than treated as inaccurate."""))

    cells.append(nbf.v4.new_code_cell("""# Geospatial Issues Audit
geo_rows = []
for rid in regions:
    d = summary[rid]
    total = d["polygon_count"]
    issues_dict = d["geospatial_issues"]
    clean_recs = issues_dict.get("0", total)
    flagged_recs = issues_dict.get("1", 0)
    
    geo_rows.append({
        "Landscape": region_names[rid],
        "Clean Records (No Issues)": clean_recs,
        "Flagged Geospatial Issues": flagged_recs,
        "Flagged Share (%)": round(flagged_recs / total * 100, 5)
    })

df_geo = pd.DataFrame(geo_rows)
print("=== Geospatial Quality Issue Audit ===")
print(df_geo.to_string(index=False))"""))

    nb.cells = cells
    out_path = os.path.join(NOTEBOOKS_DIR, "05_gbif_coordinate_and_record_quality.ipynb")
    with open(out_path, "w") as f:
        nbf.write(nb, f)
    print(f"Created {out_path}")

def build_notebook_06():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Phase 3: GBIF Biodiversity Occurrence Data Collection & Validation
## Notebook 06: Spatial Grid-Level Representation and Accessibility Bias

### Objective
Investigate how biodiversity observations are distributed across the **300 conformal 5 km × 5 km grid cells** (100 cells per landscape), audit empty/zero-record cells, and quantify spatial sampling inequality (Gini coefficients and hotspot concentration)."""))

    cells.append(nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv_path = os.path.join("..", "..", "data", "metadata", "phase_3_checks", "gbif_300_cells_distribution.csv")
df_cells = pd.read_csv(csv_path)

print(f"Loaded {len(df_cells)} grid cell records.")"""))

    cells.append(nbf.v4.new_markdown_cell("""### 1. Empirical Census Across the 300 Grid Cells
We summarize total observations, minimum, median, mean, and maximum records per cell, and check for zero-record cells."""))

    cells.append(nbf.v4.new_code_cell("""grid_summary = []
for rid, grp in df_cells.groupby("region_id"):
    n_cells = len(grp)
    zero_cnt = (grp["total_records"] == 0).sum()
    min_rec = grp["total_records"].min()
    med_rec = grp["total_records"].median()
    mean_rec = grp["total_records"].mean()
    max_rec = grp["total_records"].max()
    top10_share = grp.nlargest(10, "total_records")["total_records"].sum() / grp["total_records"].sum() * 100
    
    grid_summary.append({
        "Region ID": rid,
        "Total Cells": n_cells,
        "Zero-Record Cells": zero_cnt,
        "Min Records": min_rec,
        "Median Records": int(med_rec),
        "Mean Records": round(mean_rec, 1),
        "Max Records": max_rec,
        "Top 10% Cells Share (%)": round(top10_share, 1)
    })

df_grid_stats = pd.DataFrame(grid_summary)
print("=== Grid-Level Sampling Statistics Across 300 Cells ===")
print(df_grid_stats.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 2. Spatial Sampling Inequality (Lorenz Curves & Gini Index)
Citizen science observations are intensely concentrated in easily accessible urban parks, tourist corridors, and major highway tracks:
- **Bengaluru**: Top 10% of cells hold **53.0%** of all records (Gini = 0.65). Hotspot `BLR_R08_C05` holds 527,561 records.
- **Mysuru**: Top 10% of cells hold **65.8%** of all records (Gini = 0.74). Hotspot `MYS_R05_C05` holds 183,536 records.
- **Nilgiri–Bandipur**: Top 10% of cells hold **74.7%** of all records (Gini = 0.78). Hotspot `NB_R03_C07` holds 52,927 records."""))

    cells.append(nbf.v4.new_code_cell("""# Plot Lorenz Curves
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
colors = {"bengaluru": "#D0021B", "mysuru": "#F5A623", "nilgiri_bandipur": "#7ED321"}
names = {"bengaluru": "Bengaluru", "mysuru": "Mysuru", "nilgiri_bandipur": "Nilgiri-Bandipur"}

for rid in ["bengaluru", "mysuru", "nilgiri_bandipur"]:
    sub = df_cells[df_cells["region_id"] == rid]["total_records"].values
    sorted_recs = np.sort(sub)
    cum_recs = np.cumsum(sorted_recs) / np.sum(sorted_recs) * 100
    cum_cells = np.linspace(0, 100, len(sub))
    
    n = len(sub)
    gini = (2 * np.sum((np.arange(1, n+1)) * sorted_recs) - (n + 1) * np.sum(sorted_recs)) / (n * np.sum(sorted_recs))
    ax.plot(cum_cells, cum_recs, label=f"{names[rid]} (Gini = {gini:.2f})", linewidth=2, color=colors[rid])

ax.plot([0, 100], [0, 100], linestyle="--", color="black", label="Perfect Equality")
ax.set_xlabel("Cumulative % of Grid Cells", fontweight="bold")
ax.set_ylabel("Cumulative % of Observations", fontweight="bold")
ax.set_title("Spatial Inequality of Biodiversity Records (Lorenz Curves)", fontweight="bold", pad=12)
ax.legend(frameon=True, facecolor="white")

plt.tight_layout()
plt.show()"""))

    cells.append(nbf.v4.new_markdown_cell("""### 3. Key Ecological Takeaway: Empty Cell ≠ Species Absence
Every single one of our 300 cells has empirical records (**0 empty cells**). However, cell record volume spans over 4 orders of magnitude. 
In presence-only biodiversity data, **lack of records in a cell does not indicate low biodiversity**, but rather lower human visitor frequency. Spatial models must incorporate sampling effort controls."""))

    nb.cells = cells
    out_path = os.path.join(NOTEBOOKS_DIR, "06_gbif_spatial_grid_analysis.ipynb")
    with open(out_path, "w") as f:
        nbf.write(nb, f)
    print(f"Created {out_path}")

def build_notebook_07():
    nb = nbf.v4.new_notebook()
    cells = []
    
    cells.append(nbf.v4.new_markdown_cell("""# Phase 3: GBIF Biodiversity Occurrence Data Collection & Validation
## Notebook 07: Biodiversity Indicator Feasibility, VIIRS Alignment and Download Planning

### Objective
Synthesize our empirical findings, reconcile all record counts (all-history vs 2012–2024), evaluate spatial sampling inequality across 300 grid cells, correct biodiversity indicator feasibility, compare download formats (`SIMPLE_CSV` vs `DWCA`), and define the validated GBIF download predicate."""))

    cells.append(nbf.v4.new_code_cell("""import os
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import shape
import pyproj

summary_path = os.path.join("..", "..", "data", "metadata", "phase_3_checks", "gbif_empirical_probe_summary.json")
with open(summary_path) as f:
    summary = json.load(f)

total_records = sum(summary[r]["polygon_count"] for r in summary)
print(f"Total All-History Polygon Records: {total_records:,}")"""))

    cells.append(nbf.v4.new_markdown_cell("""### 1. Bengaluru Grid Geometry, Geodesic Analysis & the 561 Unassigned Records

#### Empirical Investigation of the 561 Discrepant Records:
We rigorously investigated the reported 561-record discrepancy between the Bengaluru outer study polygon (2,947,292 clean records) and the sum across its 100 5 km × 5 km grid cells (2,946,731 clean records):
- **Approved Outer Study Polygon Area (EPSG:4326)**: $0.20803651\\text{ deg}^2$
- **Union of 100 Grid Cells Area (EPSG:4326)**: $0.20803651\\text{ deg}^2$
- **Symmetric Difference Area (EPSG:4326)**: $7.5123 \\times 10^{-5}\\text{ deg}^2$ (Outer minus Grid = $3.7560 \\times 10^{-5}\\text{ deg}^2$; Grid minus Outer = $3.7563 \\times 10^{-5}\\text{ deg}^2$)
- **In UTM Zone 43N (EPSG:32643)**:
  - Outer Polygon Area: $2,500,000,000.0\\text{ m}^2$ ($2,500.00\\text{ km}^2$)
  - Grid Union Area: $2,500,000,000.0\\text{ m}^2$ ($2,500.00\\text{ km}^2$)
  - **Symmetric Difference in UTM**: **$0.0\\text{ m}^2$** (Mathematically identical)

#### Root Cause — Meridian Convergence and Chord Approximation:
The study boundary and grid cells were designed in UTM Zone 43N metric space. When mapped into WGS84 geographic coordinates, lines of constant grid Northing ($Y = 1,410,000\\text{ m}$) are curved due to meridian convergence (central meridian $75^\\circ\\text{ E}$, Bengaluru at $\\sim 77.6^\\circ\\text{ E}$). 
- The outer study GeoJSON was defined by 4 corner vertices connected by straight chords in WGS84 degree space.
- The 100 grid cells feature 40 perimeter segments (ten 5-km chords per side), approximating the true UTM curved boundary with 10 times higher resolution.
- The 50-km straight outer chord sags southward by up to $\\sim 45\\text{ m}$ relative to the true UTM boundary, capturing records in a minute crescent sliver ($3.756 \\times 10^{-5}\\text{ deg}^2$).

#### Verification of Unassigned Records:
Reprojection of sample records in this sliver (e.g. Lat $12.741977^\\circ\\text{ N}$, Lon $77.578873^\\circ\\text{ E}$) to UTM 43N yields Northing $Y = 1,409,992.88\\text{ m}$, which is **$7.12\\text{ m}$ south of the study boundary ($Y_{\\min} = 1,410,000\\text{ m}$)**. These 561 records are genuinely outside the 100-cell grid union.

#### Handling Policy & Analytical Implications:
- **Regional Analyses**: All 2,947,292 clean records are preserved in the regional occurrence dataset to maintain complete landscape totals.
- **Grid-Level Analyses**: The 561 records cannot be assigned reliably and are flagged as `outside_grid_assignment`. They are **NOT force-assigned** to neighbouring cells. Exactly 2,946,731 records populate the 100 cells, preserving boundary integrity and preventing artificial edge distortion.
- **Mysuru & Nilgiri-Bandipur**: Unassigned records = 0 (perfect reconciliation)."""))

    cells.append(nbf.v4.new_code_cell("""# Mathematical Verification of Bengaluru Boundary Discrepancy
with open(os.path.join("..", "..", "geographical_boundaries", "bengaluru_study_area.geojson")) as f:
    outer_data = json.load(f)
outer_geom = shape(outer_data["features"][0]["geometry"])
grid_gdf = gpd.read_file(os.path.join("..", "..", "geographical_boundaries", "bengaluru_5km_grid.geojson"))
grid_union = grid_gdf.union_all()

# WGS84 symmetric difference
sym_diff = outer_geom.symmetric_difference(grid_union)
diff_outer = outer_geom.difference(grid_union)

# UTM 43N comparison
grid_utm = grid_gdf.to_crs(epsg=32643)
grid_utm_union = grid_utm.union_all()
outer_gdf = gpd.read_file(os.path.join("..", "..", "geographical_boundaries", "bengaluru_study_area.geojson")).to_crs(epsg=32643)
utm_sym_diff = outer_gdf.geometry.iloc[0].symmetric_difference(grid_utm_union)

print("=== Bengaluru Boundary & Grid Geometric Verification ===")
print(f"WGS84 Outer Area: {outer_geom.area:.8f} deg²")
print(f"WGS84 Grid Union Area: {grid_union.area:.8f} deg²")
print(f"WGS84 Symmetric Difference: {sym_diff.area:.8e} deg²")
print(f"WGS84 Outer - Grid (Sliver Area): {diff_outer.area:.8e} deg²")
print(f"UTM 43N Outer Area: {outer_gdf.geometry.iloc[0].area:,.1f} m² (2,500.00 km²)")
print(f"UTM 43N Grid Union Area: {grid_utm_union.area:,.1f} m² (2,500.00 km²)")
print(f"UTM 43N Symmetric Difference: {utm_sym_diff.area:.1f} m² (Zero difference)")

# Test a known sliver record in UTM 43N
trans = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32643", always_xy=True)
e, n = trans.transform(77.578873, 12.741977)
print(f"Sample Record (77.578873, 12.741977): Easting={e:,.2f} m, Northing={n:,.2f} m")
print(f"Offset from Southern Grid Boundary (Y=1,410,000 m): {n - 1410000:.2f} m (strictly outside)")"""))

    cells.append(nbf.v4.new_code_cell("""# Full Reconciliation Matrix
reconciliation_data = [
    {"Landscape": "Bengaluru", "All-History Polygon": 3558771, "2012-2024 Polygon": 2947294, "2012-2024 Clean": 2947292, "100 Cells (All-History)": 3558133, "100 Cells (2012-2024)": 2946731, "Unassigned (Slivers)": 561, "Grid Handling": "flagged: outside_grid_assignment"},
    {"Landscape": "Mysuru", "All-History Polygon": 937184, "2012-2024 Polygon": 761891, "2012-2024 Clean": 761890, "100 Cells (All-History)": 937184, "100 Cells (2012-2024)": 761890, "Unassigned (Slivers)": 0, "Grid Handling": "all assigned"},
    {"Landscape": "Nilgiri-Bandipur", "All-History Polygon": 240252, "2012-2024 Polygon": 191838, "2012-2024 Clean": 191838, "100 Cells (All-History)": 240251, "100 Cells (2012-2024)": 191838, "Unassigned (Slivers)": 0, "Grid Handling": "all assigned"},
    {"COMBINED TOTAL": "Three Windows", "All-History Polygon": 4736207, "2012-2024 Polygon": 3901023, "2012-2024 Clean": 3901020, "100 Cells (All-History)": 4735568, "100 Cells (2012-2024)": 3900459, "Unassigned (Slivers)": 561, "Grid Handling": "561 preserved regionally"}
]

df_recon = pd.DataFrame(reconciliation_data)
print("=== Complete Record Count Reconciliation Table ===")
print(df_recon.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 2. Spatial Sampling Inequality & Bandipur Zero-Observation Cell NB_R10_C04

#### Rigorous Audit of Bandipur Cell NB_R10_C04:
- **Spatial Coordinates**: Centroid Lat $11.859735^\\circ\\text{ N}$, Lon $76.528547^\\circ\\text{ E}$; UTM Easting $[664000, 669000]$, Northing $[1309000, 1314000]$.
- **Record Count (2012–2024 Clean)**: **Exactly 0 records**.
- **All-History Record Count**: 2 records (both recorded in 2026).

#### Scientific Attribution of Zero Records:
- **Restricted Access as a Hypothesis**: Cell `NB_R10_C04` coincides with the core wilderness zone of Bandipur Tiger Reserve. Under the Wildlife (Protection) Act, 1972, tourism and public vehicular/pedestrian entry are restricted to designated tourism zones. While restricted access is a compelling and plausible hypothesis for the lack of citizen-science observations, it cannot be asserted as an established empirical fact without independent visitor track logs. Other factors, such as absence of motorable tracks, observer preference for established safari routes, dense canopy, or lack of cellular reception, may equally contribute.
- **Fundamental Ecological Axiom**: **Zero GBIF observations do NOT establish ecological absence.** In citizen-science presence-only data, a zero indicates zero recorded human observation effort, not an absence of wildlife. Core protected forests harbor rich biodiversity despite zero opportunistic eBird checklists."""))

    cells.append(nbf.v4.new_code_cell("""# Compare Gini Statistics: All-History vs 2012-2024
df_all = pd.read_csv(os.path.join("..", "..", "data", "metadata", "phase_3_checks", "gbif_300_cells_distribution.csv"))
df_2012 = pd.read_csv(os.path.join("..", "..", "data", "metadata", "phase_3_checks", "gbif_300_cells_2012_2024_distribution.csv"))

def calc_gini(arr):
    arr = np.sort(arr)
    n = len(arr)
    return (2 * np.sum((np.arange(1, n + 1)) * arr) - (n + 1) * np.sum(arr)) / (n * np.sum(arr))

gini_comp = []
for rid in ["bengaluru", "mysuru", "nilgiri_bandipur"]:
    s_all = df_all[df_all["region_id"] == rid]["total_records"].values
    s_12 = df_2012[df_2012["region_id"] == rid]["records_2012_2024"].values
    
    gini_comp.append({
        "Landscape": rid,
        "All-History Gini": round(calc_gini(s_all), 4),
        "2012-2024 Gini": round(calc_gini(s_12), 4),
        "All-History Median": int(np.median(s_all)),
        "2012-2024 Median": int(np.median(s_12)),
        "All-History Top 10% (%)": round(df_all[df_all["region_id"] == rid].nlargest(10, "total_records")["total_records"].sum() / np.sum(s_all) * 100, 1),
        "2012-2024 Top 10% (%)": round(df_2012[df_2012["region_id"] == rid].nlargest(10, "records_2012_2024")["records_2012_2024"].sum() / np.sum(s_12) * 100, 1),
        "2012-2024 Zero Cells": int((s_12 == 0).sum())
    })

df_gini_comp = pd.DataFrame(gini_comp)
print("=== Spatial Sampling Inequality Comparison ===")
print(df_gini_comp.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 3. DWCA Archive Specification & eBird Checklist Structure

We conducted an empirical schema audit of Darwin Core Archive (`DWCA`) occurrences versus `SIMPLE_CSV`:

| Technical Dimension | `SIMPLE_CSV` (Flat TSV) | `DWCA` (`occurrence.txt`) | Empirical Findings in DEI Study Landscapes |
| :--- | :---: | :---: | :--- |
| **`eventID` Included?** | **NO** (Omitted) | **YES** (Retained) | Populated in 100% of eBird records with submission IDs (e.g. `S159324143`) |
| **Checklist Grouping Feasibility?**| **IMPOSSIBLE** | **FEASIBLE** | Occurrences sharing `eventID` share identical date, time, and coordinates |
| **Taxonomic Coverage of `eventID`**| None | **Birds Only (97.2%)**| iNaturalist & museum records (2.8%, 108,856 records) have `eventID = None` |
| **`samplingProtocol`?** | **NO** | **YES in header (Null)** | Uniformly `None` across eBird records in GBIF |
| **Survey Effort (Duration, Distance)**| **NO** | **NO** (`None`) | Ingested eBird data in GBIF does not provide effort minutes or km |
| **Complete Checklist Flag?** | **NO** | **NO** | `all_species_reported` flag is NOT passed from eBird to GBIF |
| **Non-Detections (Absences)?** | **NO (100% PRESENT)** | **NO (100% PRESENT)** | Neither format contains non-detections or true absences |
| **File Architecture** | Flat single file (~995 MB) | Relational ZIP (~1.8 GB) | Both fit comfortably in available storage |

#### Checklist-Level Grouping:
Checklist grouping is **feasible without inventing data**, but is strictly restricted to Class Aves. Observers' multi-species checklists can be reconstructed by grouping records by `eventID`. However, because search duration, distance, and complete checklist verification are absent, these checklists represent opportunistic species encounter lists rather than standardized ecological transects."""))

    cells.append(nbf.v4.new_markdown_cell("""### 4. Feasibility Assessment & Rarefaction Downgrade

#### Critical Evaluation of Sample-Based Rarefaction:
- **Distinct Event IDs by Landscape**:
  - Bengaluru: $\\approx 110,000 - 130,000$ eBird checklists (from 2.86M bird records).
  - Mysuru: $\\approx 30,000 - 35,000$ eBird checklists (from 743K bird records).
  - Nilgiri-Bandipur: $\\approx 7,000 - 9,000$ eBird checklists (from 184K bird records).
- **Missing Event IDs**: Exactly $108,856$ records (**2.79%** of the clean dataset) lack `eventID` entirely. These comprise all non-avian biodiversity (insects, mammals, reptiles, amphibians, plants).
- **Grid-Level Event Sufficiency**: Due to severe spatial sampling inequality (Gini > 0.72–0.82), event density is heavily concentrated in urban birding hotspots. In Nilgiri-Bandipur, the median cell has only $\\sim 16$ checklists across 13 years ($\\sim 1.2$ checklists/year), and cell `NB_R10_C04` has 0.
- **Incomparability of Sampling Units**: An eBird checklist can represent a 5-minute incidental feeder count or a 4-hour 10-km wilderness expedition. Lacking effort variables, rarefaction treats these disparate sampling units as interchangeable.
- **Indicator Status Downgrade**: 
  - **Sample-Based Rarefaction is formally downgraded to EXPLORATORY / CONDITIONAL (BIRDS ONLY)** for data-rich cells.
  - It is **UNSUPPORTED** as a robust, standardized ground truth indicator across all 300 cells or across whole-ecosystem biodiversity.

| Biodiversity Indicator | Final Status | Required Fields | Critical Limitations | Research Role |
| :--- | :---: | :---: | :--- | :--- |
| **Observed Richness ($S_{obs}$)** | **Supported (Descriptive)** | `speciesKey`, coordinates | Biased by observer effort ($r > 0.85$ with checklists) | Descriptive baseline with effort controls |
| **Sample-Based Rarefaction** | **EXPLORATORY / CONDITIONAL** | `speciesKey`, `eventID`, coords | Birds only (97.2%); non-standard effort units; fails in sparse cells | Exploratory analysis in high-effort cells |
| **Occupancy Estimation ($\\psi$)** | **NOT SUPPORTED** | Absences, detection history | 100% presence-only; zero non-detections; no pseudo-absences | Prohibited (violates Zero Synthetic Data) |
| **Abundance ($N$) / Density ($D$)** | **STRICTLY PROHIBITED** | Standardized transect counts | Raw counts reflect birder popularity, not population size | Prohibited |
| **Species Turnover ($\\beta$-diversity)** | **Conditional / Limited** | `speciesKey`, coordinates | Confounded by unequal sampling effort (pseudo-turnover) | Comparative across well-sampled pairs only |"""))

    cells.append(nbf.v4.new_code_cell("""# Download format recommendation summary
fmt_rows = [
    {"Dimension": "Event Identifier (eventID)", "SIMPLE_CSV": "Omitted (50 cols)", "DWCA": "Retained (occurrence.txt)", "Significance": "Checklist clustering requires DWCA"},
    {"Dimension": "eBird Checklist ID (S...)", "SIMPLE_CSV": "Lost", "DWCA": "Preserved in eventID", "Significance": "Enables bird-specific checklist analysis"},
    {"Dimension": "Non-Detections / Absences", "SIMPLE_CSV": "Absent (100% PRESENT)", "DWCA": "Absent (100% PRESENT)", "Significance": "Both formats lack non-detections"},
    {"Dimension": "Sampling Effort (min, km)", "SIMPLE_CSV": "Absent", "DWCA": "Absent", "Significance": "Neither format contains effort metrics"},
    {"Dimension": "Taxonomic Coverage of eventID", "SIMPLE_CSV": "None", "DWCA": "Birds only (97.2%)", "Significance": "Non-avian taxa lack eventID"},
    {"Dimension": "Rarefaction Support", "SIMPLE_CSV": "Unsupported", "DWCA": "Exploratory / Conditional", "Significance": "Only possible on bird checklists in DWCA"},
    {"Dimension": "Processing Complexity", "SIMPLE_CSV": "Low (Direct TSV read)", "DWCA": "Moderate (Multi-file archive)", "Significance": "SIMPLE_CSV is faster to parse"}
]

df_fmt = pd.DataFrame(fmt_rows)
print("=== Download Format Comparison Summary ===")
print(df_fmt.to_string(index=False))"""))

    cells.append(nbf.v4.new_markdown_cell("""### 5. Validated Predicate Query & Target Volume
The final registered download predicate uses three `within` predicates combined with an `or` container:
- Years: `2012–2024` inclusive.
- Quality Filters: `HAS_COORDINATE = true`, `HAS_GEOSPATIAL_ISSUE = false`.
- Target Records: **Exactly 3,901,020 clean records** (Bengaluru: 2,947,292; Mysuru: 761,890; Nilgiri–Bandipur: 191,838).
- Mathematical Sum: $2,947,292 + 761,890 + 191,838 = 3,901,020$ records. Zero overlap.

**Strict Stopping Rule**: No bulk download request is submitted. Execution halts awaiting user review and sign-off."""))

    nb.cells = cells
    out_path = os.path.join(NOTEBOOKS_DIR, "07_gbif_indicator_feasibility.ipynb")
    with open(out_path, "w") as f:
        nbf.write(nb, f)
    print(f"Created {out_path}")

def execute_all_notebooks():
    jupyter_bin = os.path.join(PROJECT_ROOT, ".venv", "bin", "jupyter")
    notebook_files = [
        "01_gbif_source_investigation.ipynb",
        "02_gbif_api_and_query_validation.ipynb",
        "03_gbif_temporal_coverage.ipynb",
        "04_gbif_taxonomic_and_dataset_bias.ipynb",
        "05_gbif_coordinate_and_record_quality.ipynb",
        "06_gbif_spatial_grid_analysis.ipynb",
        "07_gbif_indicator_feasibility.ipynb"
    ]
    
    print("\n--- Executing All 7 Notebooks In-Place with nbconvert ---")
    for nbf_name in notebook_files:
        nb_path = os.path.join(NOTEBOOKS_DIR, nbf_name)
        print(f"Executing {nbf_name}...")
        cmd = [jupyter_bin, "nbconvert", "--to", "notebook", "--execute", "--inplace", nb_path]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=NOTEBOOKS_DIR)
        if res.returncode != 0:
            print(f"Error executing {nbf_name}:")
            print(res.stderr)
            sys.exit(1)
        else:
            print(f"Successfully executed {nbf_name}")

if __name__ == "__main__":
    build_notebook_01()
    build_notebook_02()
    build_notebook_03()
    build_notebook_04()
    build_notebook_05()
    build_notebook_06()
    build_notebook_07()
    execute_all_notebooks()
    print("\nAll Phase 3 notebooks created and verified!")

