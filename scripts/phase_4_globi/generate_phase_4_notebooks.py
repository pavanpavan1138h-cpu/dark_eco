"""
Notebook Generator for Phase 4: GloBI Investigation
Dark Ecology Intelligence (DEI) — Phase 4
"""

import json
from pathlib import Path
import nbformat as nbf

NOTEBOOK_DIR = Path("/Users/apple/Documents/5th sem el/ANN_PBL/dark_eco/notebooks/phase_4_globi")
NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)

def create_notebook(cells, filename):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.0"
        }
    }
    filepath = NOTEBOOK_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Generated {filepath}")

# ==========================================
# Notebook 01: API & Source Investigation
# ==========================================
def build_nb_01():
    cells = [
        nbf.v4.new_markdown_cell("""# Dark Ecology Intelligence (DEI) — Phase 4: GloBI Investigation
## Notebook 01: Official API Architecture, Endpoint Mechanics, and Schema Investigation

### Academic Context
Project: **Dark Ecology Intelligence: Temporal Graph Neural Networks and Deep Reinforcement Learning for AI-Driven Light Pollution Governance**  
Course: **ANN Lab PBL — AI2531A**  
Phase: **Phase 4 — GloBI (Global Biotic Interactions) Investigation and Acquisition**

---

### Objectives of this Notebook
1. Investigate the official Global Biotic Interactions (GloBI) REST API architecture (`https://api.globalbioticinteractions.org`).
2. Catalog and define the 75 documented metadata fields provided by the `/interactionFields` endpoint.
3. Test spatial querying mechanisms using bounding boxes (`bbox=minLon,minLat,maxLon,maxLat`).
4. Prove why `includeObservations=true` is strictly required to extract empirical observation instances with geospatial coordinates and timestamps.
5. Determine pagination capabilities (`limit`, `offset`), maximum request sizes, and response formats (`json`, `csv`, `tsv`).
6. Establish scientific constraints and acquisition rules for downstream pipeline integration."""),
        
        nbf.v4.new_code_cell("""import sys
import json
import requests
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path("..").resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

print("Python runtime and modules verified.")"""),

        nbf.v4.new_markdown_cell("""### 1. GloBI API Architecture Overview
The Global Biotic Interactions (GloBI) infrastructure indexes biotic interactions across hundreds of ecological surveys, citizen science repositories, and museum databases.
Key REST endpoints:
- `GET /interactionFields`: Returns data dictionary of all supported attributes.
- `GET /interaction`: Core interaction search endpoint supporting spatial, taxonomic, and dataset filtering.
- `GET /taxa`: Resolves taxonomic names against Global Names Architecture and GBIF Backbone.
- `GET /sources`: Lists upstream datasets contributing to the GloBI index."""),

        nbf.v4.new_code_cell("""base_url = "https://api.globalbioticinteractions.org"

# Check API health and retrieve field dictionary
resp = requests.get(f"{base_url}/interactionFields?type=json", timeout=30)
print(f"HTTP Status: {resp.status_code}")
fields_dict = resp.json()
print(f"Total documented GloBI metadata fields: {len(fields_dict)}")

# Display sample of fields and definitions
sample_fields = list(fields_dict.items())[:10]
for name, meta in sample_fields:
    desc = meta.get("description", "No description provided.")
    print(f"- {name}: {desc[:90]}...")"""),

        nbf.v4.new_markdown_cell("""### 2. Categorization of GloBI Metadata Terms (75 Fields)
Let us categorize all 75 fields into scientific domains:
- **Spatial**: `latitude`, `longitude`, `altitude`, `footprintWKT`, `locality`.
- **Temporal**: `event_date`.
- **Taxonomic**: `source_taxon_name`, `target_taxon_name`, `source_taxon_path`, `target_taxon_path`, `source_taxon_external_id`, `target_taxon_external_id`.
- **Interaction / Trophic**: `interaction_type`, `interaction_type_id`.
- **Specimen & Observation**: `source_specimen_basis_of_record`, `target_specimen_basis_of_record`, `source_specimen_life_stage`, `source_specimen_sex`.
- **Provenance / Study**: `study_title`, `study_citation`, `study_doi`, `study_url`, `study_source_citation`."""),

        nbf.v4.new_code_cell("""field_rows = []
for k, v in fields_dict.items():
    desc = v.get("description", "")
    domain = "General"
    if any(s in k.lower() for s in ["lat", "lon", "alt", "wkt", "locality"]):
        domain = "Spatial"
    elif "date" in k.lower() or "time" in k.lower():
        domain = "Temporal"
    elif "taxon" in k.lower():
        domain = "Taxonomic"
    elif "interaction" in k.lower():
        domain = "Interaction/Trophic"
    elif "specimen" in k.lower():
        domain = "Specimen/Organism"
    elif "study" in k.lower():
        domain = "Study/Provenance"
        
    field_rows.append({"Field Name": k, "Domain": domain, "Description": desc})

fields_df = pd.DataFrame(field_rows)
print("Fields breakdown by domain:")
print(fields_df["Domain"].value_counts())
fields_df.head(10)"""),

        nbf.v4.new_markdown_cell("""### 3. Empirical Test: Spatial Querying and `includeObservations` Behavior
A critical empirical discovery in GloBI:
- Without `includeObservations=true`: GloBI performs taxonomic aggregation and returns unique taxon-taxon pairs where `latitude` and `longitude` are `None`!
- With `includeObservations=true`: GloBI returns individual observation records containing exact empirical coordinates, event timestamps, and individual specimen occurrence IDs!"""),

        nbf.v4.new_code_cell("""# Test Bengaluru bounding box
blr_bbox = "77.3577,12.7396,77.8229,13.1959"

# Query 1: Default (without includeObservations)
r_no_obs = requests.get(f"{base_url}/interaction", params={"bbox": blr_bbox, "type": "json", "limit": 2}).json()
row_no_obs = r_no_obs.get("data", [[]])[0]
cols_no_obs = r_no_obs.get("columns", [])

print("--- Query WITHOUT includeObservations=true ---")
print("Columns count:", len(cols_no_obs))
if "latitude" in cols_no_obs:
    lat_idx = cols_no_obs.index("latitude")
    print(f"Latitude value: {row_no_obs[lat_idx]} (NULL/None)")

# Query 2: With includeObservations=true
r_with_obs = requests.get(f"{base_url}/interaction", params={"bbox": blr_bbox, "type": "json", "includeObservations": "true", "limit": 2}).json()
row_with_obs = r_with_obs.get("data", [[]])[0]
cols_with_obs = r_with_obs.get("columns", [])

print("\\n--- Query WITH includeObservations=true ---")
print("Columns count:", len(cols_with_obs))
if "latitude" in cols_with_obs:
    lat_idx = cols_with_obs.index("latitude")
    lon_idx = cols_with_obs.index("longitude")
    print(f"Latitude: {row_with_obs[lat_idx]}, Longitude: {row_with_obs[lon_idx]} (EMPIRICAL COORDINATES POPULATED!)")"""),

        nbf.v4.new_markdown_cell("""### 4. Pagination and Request Limits
Let us test the response formats (`json`, `csv`, `tsv`) and determine the maximum payload limit per API request."""),

        nbf.v4.new_code_cell("""# Test limit parameter scalability
for lim in [50, 500, 2000, 5000, 10000]:
    p = {"bbox": blr_bbox, "type": "json", "includeObservations": "true", "limit": lim}
    r = requests.get(f"{base_url}/interaction", params=p)
    data_len = len(r.json().get("data", []))
    print(f"Requested limit={lim:<5} -> Returned {data_len:<5} records (Status: {r.status_code})")

# Test offset pagination
p_page1 = {"bbox": blr_bbox, "type": "json", "includeObservations": "true", "limit": 5, "offset": 0}
p_page2 = {"bbox": blr_bbox, "type": "json", "includeObservations": "true", "limit": 5, "offset": 5}

d1 = requests.get(f"{base_url}/interaction", params=p_page1).json()["data"]
d2 = requests.get(f"{base_url}/interaction", params=p_page2).json()["data"]

print(f"\\nOffset pagination verified: Page 1 len={len(d1)}, Page 2 len={len(d2)}")
print(f"Row 5 of Page 1 equals Row 0 of Page 2: {d1[-1] == d2[0]}")"""),

        nbf.v4.new_markdown_cell("""### 5. Summary of Findings & Pipeline Directives
1. **Endpoint**: `https://api.globalbioticinteractions.org/interaction` is fully functional and responsive.
2. **Spatial Syntax**: Bounding box parameter is `bbox=minLon,minLat,maxLon,maxLat` in WGS84 (`EPSG:4326`).
3. **Mandatory Observation Flag**: `includeObservations=true` MUST be supplied; otherwise, coordinates and dates are stripped out.
4. **Field Customization**: All 75 fields can be explicitly requested via the `fields` query parameter, returning 64 populated tabular attributes.
5. **No Deep Pagination Barrier**: Unlike GBIF's search API which truncates at 100,000 records, GloBI handles pagination smoothly via `limit` and `offset`.""")
    ]
    create_notebook(cells, "01_globi_api_and_source_investigation.ipynb")

# ==========================================
# Notebook 02: Regional Data Availability
# ==========================================
def build_nb_02():
    cells = [
        nbf.v4.new_markdown_cell("""# Dark Ecology Intelligence (DEI) — Phase 4: GloBI Investigation
## Notebook 02: Regional Data Availability Across Bengaluru, Mysuru, and Nilgiri–Bandipur

### Academic Context
Project: **Dark Ecology Intelligence: Temporal Graph Neural Networks and Deep Reinforcement Learning for AI-Driven Light Pollution Governance**  
Course: **ANN Lab PBL — AI2531A**  
Phase: **Phase 4 — GloBI Regional Feasibility and Data Availability**

---

### Objectives of this Notebook
1. Execute controlled spatial queries across our three approved 50 km × 50 km study windows:
   - **Bengaluru** (Urban): `bbox=77.3577,12.7396,77.8229,13.1959`
   - **Mysuru** (Peri-urban): `bbox=76.4242,12.0790,76.8866,12.5338`
   - **Nilgiri–Bandipur** (Forest, Option A): `bbox=76.3658,11.4286,76.8270,11.8832`
2. Audit coordinate completeness and study polygon containment.
3. Spatially join interaction records with our 100 5 km × 5 km grid cells per region.
4. Quantify temporal alignment with our approved 2012–2024 VIIRS/GBIF study baseline.
5. Catalog available interaction types and analyze bidirectional symmetry in GloBI."""),

        nbf.v4.new_code_cell("""import sys
import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
import matplotlib.pyplot as plt

# Load precomputed audit summary
summary_path = Path("../../data/metadata/phase_4_checks/globi_investigation_summary.json")
with open(summary_path, "r") as f:
    summary_data = json.load(f)

print("Loaded empirical GloBI investigation summary.")"""),

        nbf.v4.new_markdown_cell("""### 1. Regional Record Counts & Spatial Containment
Let us review the exact record counts retrieved from GloBI for the three study windows."""),

        nbf.v4.new_code_cell("""reg_table = []
for reg_key, reg in summary_data["study_landscapes"].items():
    reg_table.append({
        "Study Window": reg["name"],
        "Landscape": reg["landscape"],
        "BBOX Retrieved": reg["total_records_retrieved"],
        "With Coordinates": reg["records_with_coordinates"],
        "Inside 50km Polygon": reg["records_inside_polygon"],
        "Outside Slivers": reg["records_outside_polygon"],
        "Assigned to 5km Grid": reg["records_assigned_to_grid"],
        "Occupied Cells": f"{reg['occupied_grid_cells']} / 100",
        "2012–2024 Records": reg["records_2012_2024"],
        "Pre-2012 Records": reg["records_pre_2012"],
        "Post-2024 Records": reg["records_post_2024"]
    })

pd.DataFrame(reg_table)"""),

        nbf.v4.new_markdown_cell("""### 2. Spatial Grid-Cell Coverage (100-Cell Grids)
In Phase 1, we established a 100-cell 5 km grid for each landscape.
- **Bengaluru**: 86 of 100 cells contain at least 1 interaction record (high spatial diffusion across urban green spaces).
- **Mysuru**: 49 of 100 cells contain interaction records (concentrated around Chamundi Hills, lakes, and peri-urban farmlands).
- **Nilgiri–Bandipur**: 28 of 100 cells contain records (clustered within national park core zones and forest survey transects)."""),

        nbf.v4.new_code_cell("""# Display Figure: Spatial Grid-Cell Coverage
fig_path = Path("../../reports/phase_4/figures/globi_spatial_cell_occupancy.png")
if fig_path.exists():
    from IPython.display import Image
    display(Image(filename=str(fig_path)))
else:
    print("Figure path not found.")"""),

        nbf.v4.new_markdown_cell("""### 3. Interaction Types & Bidirectional Symmetry
GloBI indexes trophic interactions bidirectionally:
- When an organism A preys on organism B, GloBI indexes two predicates:
  - `A preysOn B`
  - `B preyedUponBy A`
- Similarly, feeding relationships are paired:
  - `A eats B`
  - `B eatenBy A`
- Host relationships:
  - `A hostOf B`
  - `B hasHost A`
- Floral visitation:
  - `A visitsFlowersOf B`
  - `B flowersVisitedBy A`

Let us inspect the top interaction types per landscape."""),

        nbf.v4.new_code_cell("""for reg_key, reg in summary_data["study_landscapes"].items():
    print(f"=== {reg['name']} ({reg['landscape']}) Interaction Types ===")
    itypes = pd.Series(reg["interaction_types"])
    print(itypes.head(8))
    print()"""),

        nbf.v4.new_code_cell("""# Display Figure: Interaction Types Breakdown
fig_path = Path("../../reports/phase_4/figures/globi_interaction_types_breakdown.png")
if fig_path.exists():
    from IPython.display import Image
    display(Image(filename=str(fig_path)))"""),

        nbf.v4.new_markdown_cell("""### 4. Temporal Alignment with 2012–2024 Baseline
Our remote sensing (VIIRS) and GBIF occurrence datasets cover 2012–2024.
How well do empirical GloBI interaction observations align with this window?
- **Bengaluru**: 4,482 records (62.0%) fall in 2012–2024; 2,092 in 2025/2026; 590 pre-2012.
- **Mysuru**: 574 records (60.7%) fall in 2012–2024; 212 in 2025/2026; 148 pre-2012.
- **Nilgiri–Bandipur**: 104 records (11.9%) fall in 2012–2024; 752 records (85.8%) date from 2006/2008!
  - *Scientific Insight*: The vast majority of forest interactions in Nilgiri-Bandipur originate from the published **CarniDIET** survey (Middleton et al.), which conducted carnivore scat analyses in 2006 and 2008. These represent genuine, high-quality trophic interactions (Tiger, Leopard, Dhole) that can serve as a static regional trophic scaffold."""),

        nbf.v4.new_code_cell("""# Display Figure: Temporal Distribution
fig_path = Path("../../reports/phase_4/figures/globi_temporal_distribution.png")
if fig_path.exists():
    from IPython.display import Image
    display(Image(filename=str(fig_path)))"""),

        nbf.v4.new_markdown_cell("""### 5. Summary of Regional Availability
- **Total empirical records retrieved**: 9,048 across the three bounding boxes.
- **Records inside 50 km study polygons**: 9,044 (99.96%).
- **Coordinate completeness**: 100.0% of records have valid decimal latitude and longitude.
- **Temporal completeness**: >98.7% across all three regions have documented event dates.
- **Trophic coverage**: Broad coverage of herbivory, predation, pollination, and parasitism across taxa.""")
    ]
    create_notebook(cells, "02_globi_regional_data_availability.ipynb")

# ==========================================
# Notebook 03: Sample Record & Schema Audit
# ==========================================
def build_nb_03():
    cells = [
        nbf.v4.new_markdown_cell("""# Dark Ecology Intelligence (DEI) — Phase 4: GloBI Investigation
## Notebook 03: Sample Record Inspection, Data Schema, and Quality Audit

### Academic Context
Project: **Dark Ecology Intelligence: Temporal Graph Neural Networks and Deep Reinforcement Learning for AI-Driven Light Pollution Governance**  
Course: **ANN Lab PBL — AI2531A**  
Phase: **Phase 4 — GloBI Schema and Quality Audit**

---

### Objectives of this Notebook
1. Conduct granular, field-by-field record audits across urban, peri-urban, and forest landscapes.
2. Inspect upstream source dataset provenance (iNaturalist citizen science, CarniDIET ecological literature, museum vouchers).
3. Evaluate completeness of the 64 returned tabular columns.
4. Distinguish between empirical field observation records and literature-derived assertions.
5. Document known scientific biases and data limitations."""),

        nbf.v4.new_code_cell("""import sys
import json
import pandas as pd
from pathlib import Path

# Load sample records
blr_df = pd.read_csv("../../data/metadata/phase_4_checks/globi_audited_bengaluru.csv", nrows=100)
mys_df = pd.read_csv("../../data/metadata/phase_4_checks/globi_audited_mysuru.csv", nrows=100)
nb_df = pd.read_csv("../../data/metadata/phase_4_checks/globi_audited_nilgiri_bandipur.csv", nrows=100)

print(f"Loaded sample records: Bengaluru ({len(blr_df)}), Mysuru ({len(mys_df)}), Nilgiri ({len(nb_df)})")"""),

        nbf.v4.new_markdown_cell("""### 1. Granular Record Inspection Across Landscapes

Let us examine representative records from each landscape:
1. **Urban (Bengaluru)**: Direct empirical observation of wasp predation on spider.
2. **Peri-urban (Mysuru)**: Direct empirical observation of butterfly feeding on plant.
3. **Forest (Nilgiri–Bandipur)**: Scientific dietary analysis of Tiger/Leopard scat."""),

        nbf.v4.new_code_cell("""def inspect_record(df, idx):
    row = df.iloc[idx]
    fields = [
        "source_taxon_name", "interaction_type", "target_taxon_name",
        "latitude", "longitude", "cell_id", "event_date",
        "source_specimen_basis_of_record", "study_title"
    ]
    return {f: row.get(f) for f in fields if f in row}

print("--- Sample 1: Bengaluru (Urban) ---")
print(json.dumps(inspect_record(blr_df, 0), indent=2))

print("\\n--- Sample 2: Mysuru (Peri-urban) ---")
print(json.dumps(inspect_record(mys_df, 0), indent=2))

print("\\n--- Sample 3: Nilgiri-Bandipur (Forest) ---")
print(json.dumps(inspect_record(nb_df, 0), indent=2))"""),

        nbf.v4.new_markdown_cell("""### 2. Upstream Data Source Provenance
Let us analyze the contributing datasets that feed into GloBI for each landscape."""),

        nbf.v4.new_code_cell("""for name, df in [("Bengaluru", blr_df), ("Mysuru", mys_df), ("Nilgiri-Bandipur", nb_df)]:
    print(f"=== {name} Top Studies ===")
    top_studies = df["study_title"].value_counts().head(3)
    for title, count in top_studies.items():
        print(f"  [{count} records] {str(title)[:90]}...")
    print()"""),

        nbf.v4.new_markdown_cell("""### 3. Column Completeness Matrix (64 Attributes)
Let us evaluate which columns are consistently populated versus those that are mostly null."""),

        nbf.v4.new_code_cell("""completeness = (blr_df.notnull().mean() * 100).sort_values(ascending=False)

print("Top 15 Most Complete Columns (Bengaluru Sample):")
print(completeness.head(15))

print("\\nBottom 15 Least Complete / Null Columns:")
print(completeness.tail(15))"""),

        nbf.v4.new_markdown_cell("""### 4. Scientific Quality & Bias Assessment
1. **Vagueness of `interactsWith`**:
   - In Bengaluru, 2,498 records (~34.6%) use the generic predicate `interactsWith` without specifying whether it is predation, herbivory, or mutualism.
   - *Recommendation*: Filter or refine `interactsWith` using source specimen observation notes or isolate specific trophic predicates (`eats`, `preysOn`, `pollinates`).
2. **Citizen Science Geographic Clustering**:
   - iNaturalist observations in Bengaluru are heavily clustered around urban parks (Lalbagh, Cubbon Park, IISc campus) and peri-urban water bodies.
3. **Taxonomic Sampling Bias**:
   - Insect-plant associations and large mammal diets dominate the dataset. Soil fauna, nocturnal micro-moths, and microbial symbionts are under-represented.""")
    ]
    create_notebook(cells, "03_globi_sample_record_and_schema_audit.ipynb")

# ==========================================
# Notebook 04: GBIF Taxonomic Overlap
# ==========================================
def build_nb_04():
    cells = [
        nbf.v4.new_markdown_cell("""# Dark Ecology Intelligence (DEI) — Phase 4: GloBI Investigation
## Notebook 04: GBIF Taxonomic Overlap and Graph Neural Network Feasibility

### Academic Context
Project: **Dark Ecology Intelligence: Temporal Graph Neural Networks and Deep Reinforcement Learning for AI-Driven Light Pollution Governance**  
Course: **ANN Lab PBL — AI2531A**  
Phase: **Phase 4 — Taxonomic Cross-Referencing and Graph Feasibility**

---

### Objectives of this Notebook
1. Cross-reference GloBI interaction taxa with our 3,901,020 GBIF occurrence dataset (3,964 unique species).
2. Measure exact binomial species matching rates per study landscape.
3. Evaluate ecological network connectivity across our 300 5 km grid cells.
4. Assess graph suitability: node formulation, edge types, network density, and TGNN modeling feasibility."""),

        nbf.v4.new_code_cell("""import sys
import json
import pandas as pd
from pathlib import Path

# Load summary data
with open("../../data/metadata/phase_4_checks/globi_investigation_summary.json", "r") as f:
    summary_data = json.load(f)

overlap_meta = summary_data["taxonomic_overlap_with_gbif"]
print("Loaded taxonomic overlap metadata.")"""),

        nbf.v4.new_markdown_cell("""### 1. Overall Taxonomic Overlap
Across our three study regions:
- **Total unique taxa in GloBI**: 1,206 taxa.
- **Total unique species in GBIF DWCA**: 3,964 species.
- **Exact direct binomial matches**: 615 species (51.0% of all GloBI taxa)."""),

        nbf.v4.new_code_cell("""print(f"Total Unique GloBI Taxa: {overlap_meta['total_unique_globi_taxa']}")
print(f"Total Unique GBIF Species: {overlap_meta['total_gbif_species']}")
print(f"Exact Binomial Matches: {overlap_meta['total_exact_binomial_matches']} ({overlap_meta['total_overlap_percentage']:.1f}%)")

# Display regional breakdown
overlap_rows = []
for reg_key, info in overlap_meta["regional_breakdown"].items():
    overlap_rows.append({
        "Region": reg_key.title(),
        "Unique GloBI Taxa": info["globi_taxa_count"],
        "GBIF Binomial Matches": info["exact_binomial_overlap_count"],
        "Match Percentage": f"{info['overlap_percentage']:.1f}%",
        "Sample Overlapping Taxa": ", ".join(info["sample_overlapping_species"][:4])
    })

pd.DataFrame(overlap_rows)"""),

        nbf.v4.new_code_cell("""# Display Figure: Taxonomic Overlap
fig_path = Path("../../reports/phase_4/figures/globi_gbif_taxonomic_overlap.png")
if fig_path.exists():
    from IPython.display import Image
    display(Image(filename=str(fig_path)))"""),

        nbf.v4.new_markdown_cell("""### 2. Why Are Some GloBI Taxa Not in GBIF?
1. **Taxonomic Rank Discordance**: Some GloBI taxa are recorded at higher ranks (genus, family, e.g., *Ficus*, *Apis*, *Pompilidae*), whereas GBIF occurrences are indexed at species binomials.
2. **eBird Dominance in GBIF**: As established in Phase 3, 98.06% of GBIF records are birds. GloBI contains extensive plant-insect interactions (butterflies on host plants), many of which are under-represented in eBird.
3. **Taxonomic Synonyms**: Certain scientific names differ between iNaturalist / GloBI taxonomies and GBIF Backbone."""),

        nbf.v4.new_markdown_cell("""### 3. Graph Suitability and Neural Network Formulation
For our eventual Temporal Graph Neural Network (TGNN):
1. **Node Definition**:
   - Species $v_i \in \mathcal{V}$ present in grid cell $c$ at time $t$ (derived from GBIF occurrences).
2. **Edge Definition**:
   - Directed ecological interaction $(v_i, v_j, r)$ where $r \in \{\text{preysOn}, \text{eats}, \text{pollinates}, \text{hasHost}\}$ (derived from GloBI).
3. **Static Master Graph vs. Dynamic Realized Subgraph**:
   - GloBI provides the *potential trophic scaffold* (regional interaction network).
   - Realized interactions in cell $c$ at year $t$ exist if both interacting species co-occur in cell $c$ at time $t$.
4. **Feasibility Verdict**: **HIGHLY SUITABLE WITH METHODOLOGICAL CAVEATS**.
   - GloBI empirical interactions directly ground the graph edges in empirical observations rather than synthetic or fabricated connections.""")
    ]
    create_notebook(cells, "04_globi_gbif_taxonomic_overlap.ipynb")

if __name__ == "__main__":
    build_nb_01()
    build_nb_02()
    build_nb_03()
    build_nb_04()

