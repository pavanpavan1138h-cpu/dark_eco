"""
Generate Derived Aggregated Graph Edge Table with Rigorous Geospatial Containment
Dark Ecology Intelligence (DEI) — Phase 4 Validation

Implements:
1. Active canonical orientation for reciprocal pairing and asymmetric grouping.
2. Complete CarniDIET 256-instance reduction (342 canonical events -> 86 unique edges).
3. Rigorous 2D spatial polygon intersection with the approved 5x5 km grids in EPSG:32643:
   - cell_defensible: uncertainty buffer fully contained in exactly 1 cell.
   - cell_boundary_ambiguous: uncertainty buffer intersects >1 cell.
   - cell_provisional: accuracy missing, unrecorded, or > 2,500 m.
   - regional analysis: CarniDIET, vouchers, temporal outside 2012-2024, or obscured.
"""

import json
from pathlib import Path
from collections import defaultdict
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point

PROJECT_ROOT = Path("/Users/apple/Documents/5th sem el/ANN_PBL/dark_eco")
CHECKS_DIR = PROJECT_ROOT / "data/metadata/phase_4_checks"
BOUNDARIES_DIR = PROJECT_ROOT / "geographical_boundaries"

# Load iNaturalist fetched metadata
with open(CHECKS_DIR / "inat_observations_metadata.json") as f:
    inat_meta = json.load(f)

# Load grids in EPSG:32643
grids = {}
for reg in ['bengaluru', 'mysuru', 'nilgiri_bandipur']:
    p = BOUNDARIES_DIR / f"{reg}_5km_grid.geojson"
    grids[reg] = gpd.read_file(p).to_crs("EPSG:32643")

dfs = []
for reg in ['bengaluru', 'mysuru', 'nilgiri_bandipur']:
    d = pd.read_csv(CHECKS_DIR / f'globi_audited_{reg}.csv', low_memory=False)
    d['study_region'] = reg
    dfs.append(d)

df = pd.concat(dfs, ignore_index=True)
df_poly = df[df['inside_study_polygon'] == True].copy()

def extract_obs_id(r):
    s_occ = str(r.get('source_specimen_occurrence_id', ''))
    t_occ = str(r.get('target_specimen_occurrence_id', ''))
    s_cat = str(r.get('source_specimen_catalog_number', ''))
    t_cat = str(r.get('target_specimen_catalog_number', ''))
    if '/observations/' in s_occ:
        return s_occ.split('/observations/')[-1].split('?')[0].split('/')[0]
    elif '/observations/' in t_occ:
        return t_occ.split('/observations/')[-1].split('?')[0].split('/')[0]
    elif s_cat.isdigit():
        return s_cat
    elif t_cat.isdigit():
        return t_cat
    return None

df_poly['inat_obs_id'] = df_poly.apply(extract_obs_id, axis=1)

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

passive_to_active = {
    'eatenBy': 'eats',
    'preyedUponBy': 'preysOn',
    'killedBy': 'kills',
    'flowersVisitedBy': 'visitsFlowersOf',
    'visitedBy': 'visits',
    'hostOf': 'hasHost',
    'parasiteOf': 'hasParasite'
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
            
            # Canonical orientation: prefer active predicate
            if itype in passive_to_active and rj['interaction_type'] not in passive_to_active:
                chosen = rj
                partner_idx = i
            else:
                chosen = r
                partner_idx = j
            chosen['reciprocal_partner_index'] = partner_idx
            canonical_pairs.append(chosen)
            break

df_canon = pd.DataFrame(canonical_pairs)
print(f"Total canonical interaction events inside polygon: {len(df_canon)}")

# Group into aggregated graph edges
edge_groups = defaultdict(list)
for idx, r in df_canon.iterrows():
    s = str(r['source_taxon_name']).strip()
    t = str(r['target_taxon_name']).strip()
    itype = str(r['interaction_type']).strip()
    reg = r['study_region']
    lat = round(float(r['lat_float']), 6)
    lon = round(float(r['lon_float']), 6)
    dt = str(r['event_date'])
    
    if itype in passive_to_active:
        s, t = t, s
        itype = passive_to_active[itype]
        
    if itype in {'interactsWith', 'adjacentTo', 'symbiontOf'}:
        taxa_key = tuple(sorted([s.lower(), t.lower()]))
        if s.lower() > t.lower():
            s, t = t, s
    else:
        taxa_key = (s.lower(), t.lower())
        
    k = (reg, lat, lon, dt, taxa_key, itype)
    edge_groups[k].append(r)

print(f"Total unique aggregated edges: {len(edge_groups)}")

edge_rows = []
edge_counter = 1
point_cache = {}

for k, ev_list in edge_groups.items():
    reg, lat, lon, dt, taxa_key, itype = k
    first_r = ev_list[0]
    
    obs_ids = []
    studies = []
    has_obscured = False
    best_acc = None
    
    for r in ev_list:
        oid = r.get('inat_obs_id')
        if oid and str(oid).isdigit():
            im = inat_meta.get(str(oid), {})
            if im.get('obscured') is True:
                has_obscured = True
            acc = im.get('positional_accuracy')
            if acc is not None:
                if best_acc is None or acc < best_acc:
                    best_acc = acc
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
    
    # Evidence role
    if 'CarniDIET' in study_str or any(w in study_str for w in ['mycoportal', 'ecdysis', 'ummzi', 'Michigan', 'SquamataBase']):
        ev_role = "E2: Regional Context / Literature"
    elif pd.isnull(yr) or yr < 2012 or yr > 2024:
        ev_role = "E2: Historical or Post-2024 Observation"
    else:
        ev_role = "E1: Contemporary Empirical (2012-2024)"
        
    # Spatial reliability and analysis suitability
    if 'CarniDIET' in study_str or any(w in study_str for w in ['SquamataBase', 'urn:uuid', '180e6509']):
        sp_rel = "S3: Study-Site Centroid"
        suitability = "regional analysis"
        intersecting_cells = [first_r.get('cell_id', '')]
    elif any(w in study_str for w in ['mycoportal', 'ecdysis', 'ummzi', 'Michigan']):
        sp_rel = "S4: Historical / Unresolved Locality"
        suitability = "regional analysis"
        intersecting_cells = [first_r.get('cell_id', '')]
    elif 'iNaturalist' in study_str:
        if has_obscured:
            sp_rel = "S4: Obscured / Generalized Locality"
            suitability = "regional analysis"
            intersecting_cells = []
        elif not ev_role.startswith("E1"):
            sp_rel = "S2: Point Location (Temporal Baseline)"
            suitability = "regional analysis"
            intersecting_cells = [first_r.get('cell_id', '')]
        elif best_acc is None or best_acc <= 0 or best_acc > 2500:
            sp_rel = "S2: Point Location (Unverified / Broad Precision)"
            suitability = "cell_provisional"
            intersecting_cells = [first_r.get('cell_id', '')]
        else:
            cache_key = (reg, lat, lon, best_acc)
            if cache_key not in point_cache:
                pt_geom = gpd.GeoSeries([Point(lon, lat)], crs='EPSG:4326').to_crs('EPSG:32643').iloc[0]
                buf = pt_geom.buffer(best_acc)
                grid = grids[reg]
                matches = grid.sindex.query(buf, predicate='intersects')
                cells = grid.iloc[matches]['cell_id'].tolist()
                fully_contained = False
                if len(cells) == 1 and buf.within(grid[grid['cell_id'] == cells[0]].geometry.iloc[0]):
                    fully_contained = True
                point_cache[cache_key] = (fully_contained, cells)
                
            fully_contained, cells = point_cache[cache_key]
            intersecting_cells = cells
            if fully_contained:
                sp_rel = "S1: Point Location (Verified Accuracy <= 2.5km, Contained in Cell)"
                suitability = "cell_defensible"
            else:
                sp_rel = "S2: Point Location (Boundary Ambiguous)"
                suitability = "cell_boundary_ambiguous"
    else:
        sp_rel = "S4: Historical / Unresolved Locality"
        suitability = "regional analysis"
        intersecting_cells = [first_r.get('cell_id', '')]
        
    orig_itype = first_r['interaction_type']
    if orig_itype in passive_to_active:
        src_name = first_r['target_taxon_name']
        tgt_name = first_r['source_taxon_name']
        fin_itype = passive_to_active[orig_itype]
    elif orig_itype in {'interactsWith', 'adjacentTo', 'symbiontOf'}:
        s_raw = str(first_r['source_taxon_name']).strip()
        t_raw = str(first_r['target_taxon_name']).strip()
        if s_raw.lower() > t_raw.lower():
            src_name = t_raw
            tgt_name = s_raw
        else:
            src_name = s_raw
            tgt_name = t_raw
        fin_itype = orig_itype
    else:
        src_name = first_r['source_taxon_name']
        tgt_name = first_r['target_taxon_name']
        fin_itype = orig_itype
        
    edge_rows.append({
        "edge_id": f"DEI_EDGE_{reg[:3].upper()}_{edge_counter:04d}",
        "study_region": reg,
        "source_taxon_name": src_name,
        "interaction_type": fin_itype,
        "target_taxon_name": tgt_name,
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
        "analysis_suitability": suitability,
        "intersecting_cells": "; ".join(intersecting_cells)
    })
    edge_counter += 1

df_edges = pd.DataFrame(edge_rows)
output_path = CHECKS_DIR / "globi_derived_aggregated_edges.csv"
df_edges.to_csv(output_path, index=False)
print(f"Saved {len(df_edges)} edges to {output_path} successfully.")
print("\nEdge analysis suitability breakdown:")
print(df_edges['analysis_suitability'].value_counts())
print("\nEdge spatial reliability breakdown:")
print(df_edges['spatial_reliability'].value_counts())
print("\nEdge evidence role breakdown:")
print(df_edges['evidence_role'].value_counts())
