# Raw Data Archive (`data/raw/`)

This directory holds **original, unaltered research datasets** downloaded directly from official data portals, APIs, and scientific repositories.

## Subdirectories (by source / topic)
- **`osm_reference_boundaries/`**: Verified raw JSON lookup responses of administrative, park, and water boundaries from the OpenStreetMap Nominatim service.
- *(Future Phases)*:
  - `nightlights_raw/`: DMSP-OLS and VIIRS-DNB raster tiles.
  - `biodiversity_raw/`: Raw Darwin Core Archive (DwC-A) exports from GBIF and eBird Basic Dataset downloads.
  - `traits_raw/`: Original downloaded Excel/CSV files for EltonTraits, AVONET, PanTHERIA, and AmphiBIO.
  - `environmental_raw/`: Raw GeoTIFF tiles for ESA WorldCover, Hansen GFC, WorldPop, Copernicus DEM, and NetCDF files for ERA5-Land.

## Rules
- **NEVER EDIT RAW DATA**: Files here must remain identical to their downloaded state.
- **NEVER COMMIT RAW DATA**: All contents are ignored by `.gitignore` except this README.
- **DOCUMENT ACQUISITION**: Every raw download must have an accompanying entry in `data/metadata/` detailing the exact URL, timestamp, version, and SHA-256 checksum.

