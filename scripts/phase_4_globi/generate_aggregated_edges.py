"""
Generate Derived Aggregated Graph Edge Table and Spatial-Evidence Classification
Dark Ecology Intelligence (DEI) — Phase 4
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path("/Users/apple/Documents/5th sem el/ANN_PBL/dark_eco")
CHECKS_DIR = PROJECT_ROOT / "data/metadata/phase_4_checks"

dfs = []
for reg in ['bengaluru', 'mysuru', 'nilgiri_bandipur']:
    d = pd.read_csv(CHECKS_DIR / f'globi_audited_{reg}.csv')
    d['study_region'] = reg
    dfs.append(d)

df = pd.concat(dfs, ignore_index=True)
df_poly = df[df['inside_study_polygon'] == True].copy()

# Reciprocal pairing
inv_map = {
    'eats': 'eatenBy', 'eatenBy': 'eats',
    'preysOn': 'preyedUponBy', 'preyedUponBy': 'preysOn',
    'hostOf': 'hasHost', 'hasHost': 'hostOf',
    'visitsFlowersOf': 'flowersVisitedBy', 'flowersVisitedBy': 'visitsFlowersOf',
    'hasParasite': 'parasiteOf', 'parasiteOf': 'hasParasite',
    'visits': 'visitedBy', 'visitedBy': 'visits',
    'kills': 'killedBy', 'killedBy': 'kills',
    'interactsWith': 'interactsWith',
    'adjacentTo': 'adjacentTo',
    'symbiontOf': 'symbiontOf'
}

records = df_poly.to_dict('records')
matched = set()
canonical_pairs = []

for i, r in enumerate(records):
    if i in matched:
        continue
    src = str(r['source_taxon_name']).strip().lower()
    tgt = str(r['target_taxon_name']).strip().lower()
    itype = str(r['interaction_type']).strip()
    inv_t = inv_map.get(itype, itype)
    lat = round(float(r['lat_float']), 6) if pd.notnull(r['lat_float']) else None
    lon = round(float(r['lon_float']), 6) if pd.notnull(r['lon_float']) else None
    dt = str(r['event_date'])
    
    for j in range(i + 1, len(records)):
        if j in matched:
            continue
        rj = records[j]
        if (str(rj['source_taxon_name']).strip().lower() == tgt and
            str(rj['target_taxon_name']).strip().lower() == src and
            str(rj['interaction_type']).strip() == inv_t and
            round(float(rj['lat_float']), 6) == lat and
            round(float(rj['lon_float']), 6) == lon and
            str(rj['event_date']) == dt):
            matched.add(i)
            matched.add(j)
            # Add partner info to record
            r['reciprocal_partner_index'] = j
            canonical_pairs.append(r)
            break

df_canon = pd.DataFrame(canonical_pairs)
print(f"Total canonical interaction events: {len(df_canon)}")

# Group into aggregated graph edges
# Aggregation key: (study_region, round(lat, 6), round(lon, 6), event_date, sorted_taxa, interaction_type)
edge_groups = {}
for idx, r in df_canon.iterrows():
    s = str(r['source_taxon_name']).strip()
    t = str(r['target_taxon_name']).strip()
    itype = str(r['interaction_type']).strip()
    reg = r['study_region']
    lat = round(float(r['lat_float']), 6)
    lon = round(float(r['lon_float']), 6)
    dt = str(r['event_date'])
    
    # Canonical orientation
    if itype in {'interactsWith', 'adjacentTo', 'symbiontOf'}:
        taxa_key = tuple(sorted([s.lower(), t.lower()]))
        # Keep consistent order
        if s.lower() > t.lower():
            s, t = t, s
    else:
        taxa_key = (s.lower(), t.lower())
        
    k = (reg, lat, lon, dt, taxa_key, itype)
    if k not in edge_groups:
        edge_groups[k] = []
    edge_groups[k].append(r)

print(f"Total unique aggregated edges: {len(edge_groups)}")

edge_rows = []
edge_counter = 1
for k, ev_list in edge_groups.items():
    reg, lat, lon, dt, taxa_key, itype = k
    first_r = ev_list[0]
    
    # Extract contributing record IDs
    obs_ids = []
    studies = []
    for r in ev_list:
        s_id = str(r.get('target_specimen_catalog_number', '')) or str(r.get('source_specimen_catalog_number', ''))
        occ_id = str(r.get('target_specimen_occurrence_id', '')) or str(r.get('source_specimen_occurrence_id', ''))
        rep_id = s_id if s_id and s_id != 'nan' else occ_id
        if rep_id and rep_id != 'nan':
            obs_ids.append(rep_id)
        st = str(r.get('study_title', ''))[:60]
        if st not in studies:
            studies.append(st)
            
    yr = first_r['parsed_year']
    study_str = str(first_r['study_title'])
    
    # Evidence Role
    if 'CarniDIET' in study_str or any(w in study_str for w in ['mycoportal', 'ecdysis', 'ummzi', 'Michigan', 'SquamataBase']):
        ev_role = "E2: Regional Context / Literature"
    elif pd.isnull(yr) or yr < 2012 or yr > 2024:
        ev_role = "E2: Historical or Post-2024 Observation"
    else:
        ev_role = "E1: Contemporary Empirical (2012-2024)"
        
    # Spatial Reliability
    if 'CarniDIET' in study_str or any(w in study_str for w in ['SquamataBase', 'urn:uuid', '180e6509']):
        sp_rel = "S3: Study-Site Centroid"
        cell_elig = "Regional Scaffold Only (Centroid)"
    elif any(w in study_str for w in ['mycoportal', 'ecdysis', 'ummzi', 'Michigan']):
        sp_rel = "S4: Historical / Unresolved Locality"
        cell_elig = "Regional Scaffold Only (Voucher)"
    elif 'iNaturalist' in study_str:
        sp_rel = "S2: Point Location (Unknown Precision)"
        cell_elig = "Cell-Level Dynamic Analysis (with citizen science caveats)" if ev_role.startswith("E1") else "Regional Scaffold Only (Temporal)"
    else:
        sp_rel = "S4: Historical / Unresolved Locality"
        cell_elig = "Regional Scaffold Only"
        
    edge_rows.append({
        "edge_id": f"DEI_EDGE_{reg[:3].upper()}_{edge_counter:04d}",
        "study_region": reg,
        "source_taxon_name": first_r['source_taxon_name'],
        "interaction_type": itype,
        "target_taxon_name": first_r['target_taxon_name'],
        "latitude": lat,
        "longitude": lon,
        "cell_id": first_r.get('cell_id', ''),
        "event_date": dt,
        "parsed_year": yr,
        "evidence_count": len(ev_list),
        "contributing_record_ids": "; ".join(obs_ids[:5]),
        "source_studies": "; ".join(studies),
        "evidence_role": ev_role,
        "spatial_reliability": sp_rel,
        "analysis_suitability": cell_elig
    })
    edge_counter += 1

df_edges = pd.DataFrame(edge_rows)
df_edges.to_csv(CHECKS_DIR / "globi_derived_aggregated_edges.csv", index=False)
print("Saved globi_derived_aggregated_edges.csv successfully.")
print("\nEdge analysis suitability breakdown:")
print(df_edges['analysis_suitability'].value_counts())

