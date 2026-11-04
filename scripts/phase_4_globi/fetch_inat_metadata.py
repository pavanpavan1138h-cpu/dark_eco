"""
Batch iNaturalist Observation Metadata Fetcher
Dark Ecology Intelligence (DEI) — Phase 4 Validation

Retrieves positional_accuracy, geoprivacy, and obscuration status
for all 3,588 unique upstream iNaturalist observation IDs in our GloBI dataset.
"""

import json
import logging
import time
from pathlib import Path
import requests
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("inat_fetcher")

PROJECT_ROOT = Path("/Users/apple/Documents/5th sem el/ANN_PBL/dark_eco")
CHECKS_DIR = PROJECT_ROOT / "data/metadata/phase_4_checks"
OUTPUT_FILE = CHECKS_DIR / "inat_observations_metadata.json"

dfs = []
for reg in ['bengaluru', 'mysuru', 'nilgiri_bandipur']:
    d = pd.read_csv(CHECKS_DIR / f'globi_raw_{reg}.csv')
    dfs.append(d)

df = pd.concat(dfs, ignore_index=True)
inat = df[df['study_title'].str.contains('iNaturalist', na=False)].copy()

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

inat['inat_obs_id'] = inat.apply(extract_obs_id, axis=1)
unique_ids = sorted([str(x) for x in inat['inat_obs_id'].dropna().unique() if str(x).isdigit()])
logger.info(f"Total unique iNaturalist observation IDs to query: {len(unique_ids)}")

# Check if existing partial file exists
obs_metadata = {}
if OUTPUT_FILE.exists():
    try:
        with open(OUTPUT_FILE, 'r') as f:
            obs_metadata = json.load(f)
        logger.info(f"Loaded {len(obs_metadata)} existing cached observation records.")
    except Exception:
        obs_metadata = {}

remaining_ids = [oid for oid in unique_ids if oid not in obs_metadata]
logger.info(f"Remaining IDs to fetch: {len(remaining_ids)}")

BATCH_SIZE = 60
base_url = "https://api.inaturalist.org/v1/observations"

for i in range(0, len(remaining_ids), BATCH_SIZE):
    batch = remaining_ids[i:i + BATCH_SIZE]
    logger.info(f"Fetching batch {i//BATCH_SIZE + 1} / {(len(remaining_ids) + BATCH_SIZE - 1)//BATCH_SIZE} ({len(batch)} IDs)...")
    
    try:
        r = requests.get(base_url, params={'id': ','.join(batch), 'per_page': 200}, timeout=20)
        if r.status_code == 200:
            results = r.json().get('results', [])
            found_ids = set()
            for obs in results:
                oid = str(obs.get('id'))
                found_ids.add(oid)
                obs_metadata[oid] = {
                    'status': 'available',
                    'positional_accuracy': obs.get('positional_accuracy'),
                    'public_positional_accuracy': obs.get('public_positional_accuracy'),
                    'geoprivacy': obs.get('geoprivacy'),
                    'taxon_geoprivacy': obs.get('taxon_geoprivacy'),
                    'obscured': obs.get('obscured', False),
                    'uri': obs.get('uri'),
                    'species_guess': obs.get('species_guess')
                }
            # Mark missing as unavailable
            for oid in batch:
                if oid not in found_ids:
                    obs_metadata[oid] = {
                        'status': 'unavailable_or_private',
                        'positional_accuracy': None,
                        'public_positional_accuracy': None,
                        'geoprivacy': 'private_or_deleted',
                        'taxon_geoprivacy': None,
                        'obscured': True
                    }
        else:
            logger.warning(f"Batch request returned status {r.status_code}")
            for oid in batch:
                obs_metadata[oid] = {'status': f'api_error_{r.status_code}', 'obscured': None}
    except Exception as e:
        logger.error(f"Error requesting batch: {e}")
        for oid in batch:
            obs_metadata[oid] = {'status': 'request_failed', 'obscured': None}
            
    time.sleep(0.5)

with open(OUTPUT_FILE, 'w') as f:
    json.dump(obs_metadata, f, indent=2)
logger.info(f"Saved {len(obs_metadata)} total observations metadata to {OUTPUT_FILE}.")

