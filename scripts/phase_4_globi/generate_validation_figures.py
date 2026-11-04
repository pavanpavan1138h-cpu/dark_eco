"""
Generate Final Scientific Validation Figures and Metadata
Dark Ecology Intelligence (DEI) — Phase 4: GloBI Validation
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path("/Users/apple/Documents/5th sem el/ANN_PBL/dark_eco")
CHECKS_DIR = PROJECT_ROOT / "data/metadata/phase_4_checks"
FIGURES_DIR = PROJECT_ROOT / "reports/phase_4/figures"

dfs = []
for reg in ['bengaluru', 'mysuru', 'nilgiri_bandipur']:
    d = pd.read_csv(CHECKS_DIR / f'globi_audited_{reg}.csv')
    d['study_region'] = reg
    dfs.append(d)

df = pd.concat(dfs, ignore_index=True)

# 1. Figure: Coordinate Provenance Breakdown
prov_counts = {
    "Exact GPS (iNaturalist)": (df['study_title'].str.contains('iNaturalist', na=False)).sum(),
    "Reserve Centroid (CarniDIET)": (df['study_title'].str.contains('CarniDIET', na=False)).sum(),
    "Museum Locality (Vouchers)": (df['study_title'].str.contains('mycoportal|ecdysis|ummzi|Michigan', na=False)).sum(),
    "Literature / Other Archive": (~df['study_title'].str.contains('iNaturalist|CarniDIET|mycoportal|ecdysis|ummzi|Michigan', na=False)).sum()
}

fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
colors = ['#2ca02c', '#d62728', '#ff7f0e', '#1f77b4']
bars = ax.bar(prov_counts.keys(), prov_counts.values(), color=colors, edgecolor='black', width=0.55)
ax.set_ylabel("Number of Records", fontsize=11, fontweight="bold")
ax.set_title("Coordinate Provenance of Retrieved GloBI Records (N = 9,048)", fontsize=13, fontweight="bold", pad=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=15, ha='right', fontweight='bold')

for bar in bars:
    y = bar.get_height()
    pct = y / len(df) * 100
    ax.text(bar.get_x() + bar.get_width()/2, y + 100, f"{y:,}\n({pct:.1f}%)", ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
fig.savefig(FIGURES_DIR / "globi_coordinate_provenance.png", dpi=300)
plt.close()

# 2. Figure: Final Acquisition Categories (A, B, C)
def get_cat(row):
    if not row['inside_study_polygon']:
        return 'Category C'
    study = str(row['study_title'])
    yr = row['parsed_year']
    if 'CarniDIET' in study or any(k in study for k in ['mycoportal', 'ecdysis', 'ummzi', 'Michigan']):
        return 'Category B'
    if pd.isnull(yr) or yr < 2012 or yr > 2024:
        return 'Category B'
    return 'Category A'

df['cat'] = df.apply(get_cat, axis=1)

fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
regions = ['bengaluru', 'mysuru', 'nilgiri_bandipur']
reg_labels = ['Bengaluru (Urban)', 'Mysuru (Peri-urban)', 'Nilgiri–Bandipur (Forest)']
cat_a = [((df['study_region'] == r) & (df['cat'] == 'Category A')).sum() for r in regions]
cat_b = [((df['study_region'] == r) & (df['cat'] == 'Category B')).sum() for r in regions]
cat_c = [((df['study_region'] == r) & (df['cat'] == 'Category C')).sum() for r in regions]

x = np.arange(len(regions))
w = 0.25

ax.bar(x - w, cat_a, w, label='Category A: Contemporary Empirical (2012–2024)', color='#2ca02c', edgecolor='black')
ax.bar(x, cat_b, w, label='Category B: Regional Trophic Scaffold (Centroid/Historical)', color='#ff7f0e', edgecolor='black')
ax.bar(x + w, cat_c, w, label='Category C: Excluded Boundary Slivers', color='#d62728', edgecolor='black')

ax.set_ylabel("Number of Records", fontsize=11, fontweight="bold")
ax.set_title("Scientific Acquisition Classification Across Study Landscapes", fontsize=13, fontweight="bold", pad=12)
ax.set_xticks(x)
ax.set_xticklabels(reg_labels, fontweight="bold")
ax.legend(frameon=True, fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for i in range(len(regions)):
    ax.text(x[i] - w, cat_a[i] + 75, f"{cat_a[i]:,}", ha='center', fontsize=9, fontweight='bold')
    ax.text(x[i], cat_b[i] + 75, f"{cat_b[i]:,}", ha='center', fontsize=9, fontweight='bold')
    if cat_c[i] > 0:
        ax.text(x[i] + w, cat_c[i] + 75, f"{cat_c[i]:,}", ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
fig.savefig(FIGURES_DIR / "globi_acquisition_categories.png", dpi=300)
plt.close()

# 3. Figure: Endpoint Matching with GBIF
# Load canonical forward edges
forward_verbs = {'eats', 'preysOn', 'hostOf', 'visitsFlowersOf', 'visits', 'kills', 'parasiteOf'}
inverse_verbs = {'eatenBy', 'preyedUponBy', 'hasHost', 'flowersVisitedBy', 'visitedBy', 'killedBy', 'hasParasite'}

with open(CHECKS_DIR / 'gbif_species_regional_profiles.json') as f:
    gbif_meta = json.load(f)

gbif_all = set()
for sps in gbif_meta['species_by_region'].values():
    gbif_all.update(sps)

canon_edges = []
seen = set()
for idx, r in df[df['inside_study_polygon'] == True].iterrows():
    itype = r['interaction_type']
    src = str(r['source_taxon_name']).strip()
    tgt = str(r['target_taxon_name']).strip()
    if itype in forward_verbs:
        canon_edges.append(r)
    elif itype in inverse_verbs:
        pass
    else:
        k = (r['study_region'], round(float(r['lat_float']), 6), round(float(r['lon_float']), 6), str(r['event_date']), tuple(sorted([src.lower(), tgt.lower()])))
        if k not in seen:
            seen.add(k)
            canon_edges.append(r)

df_edges = pd.DataFrame(canon_edges)
src_in = df_edges['source_taxon_name'].isin(gbif_all)
tgt_in = df_edges['target_taxon_name'].isin(gbif_all)

both_m = (src_in & tgt_in).sum()
one_m = (src_in ^ tgt_in).sum()
neither_m = ((~src_in) & (~tgt_in)).sum()

fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
labels = ['Both Endpoints\nMatch GBIF', 'One Endpoint\nMatches GBIF', 'Neither Endpoint\nMatches GBIF']
vals = [both_m, one_m, neither_m]
colors = ['#59a14f', '#4e79a7', '#e15759']

wedges, texts, autotexts = ax.pie(vals, labels=labels, autopct='%1.1f%%', startangle=140,
                                  colors=colors, explode=(0.04, 0.02, 0.08),
                                  textprops={'fontweight': 'bold', 'fontsize': 10})
ax.set_title(f"Canonical Interaction Edges GBIF Endpoint Matching\n(Total Canonical Edges N = {len(df_edges):,})",
             fontsize=12, fontweight='bold', pad=10)

plt.tight_layout()
fig.savefig(FIGURES_DIR / "globi_canonical_endpoint_matching.png", dpi=300)
plt.close()

print("Generated validation figures successfully.")

