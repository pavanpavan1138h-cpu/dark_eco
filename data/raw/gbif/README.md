# Raw GBIF Occurrence Archive (`data/raw/gbif/`)

This directory stores the official registered Darwin Core Archive (`DWCA`) downloaded from GBIF for Phase 3 of the Dark Ecology Intelligence (DEI) project.

## Archive Details
- **Source**: Global Biodiversity Information Facility (GBIF)
- **Format**: `DWCA` (Darwin Core Archive, ZIP)
- **Target Spatial Windows**: Bengaluru (Urban), Mysuru (Peri-Urban), Nilgiri–Bandipur (Protected Forest)
- **Temporal Range**: 2012–2024 inclusive
- **Expected Records**: 3,901,020 clean occurrence records
- **Primary Extension**: `occurrence.txt` (230 Darwin Core interpreted terms, including `eventID`)

## Rules & Security
- Raw archives (*.zip) and extracted tables (*.txt, *.csv) are strictly excluded from Git tracking via `.gitignore`.
- Provenance and download metadata are preserved in `data/metadata/gbif_download_manifest.json`.
- Do not modify or overwrite raw downloaded archives.

