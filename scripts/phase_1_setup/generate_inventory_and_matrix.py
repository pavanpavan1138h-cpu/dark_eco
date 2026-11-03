#!/usr/bin/env python3
"""
Dark Ecology Intelligence (DEI) - Phase 1 Setup
Script: generate_inventory_and_matrix.py

Compiles the comprehensive scientific dataset inventory and regional availability
matrix for the Dark Ecology Intelligence project across Bengaluru, Mysuru, and Nilgiri-Bandipur.
Exports both CSVs to dark_eco/ and dark_eco/reports/dataset_inventory/.
"""

import csv
import os

INVENTORY_DATA = [
    # A. Nighttime Light / ALAN Data
    {
        "category": "A. Nighttime-light / ALAN",
        "dataset_name": "DMSP-OLS Nighttime Lights (Version 4)",
        "official_url": "https://www.ngdc.noaa.gov/eog/dmsp/downloadV4composites.html (also via Google Earth Engine: NOAA/DMSP-OLS/NIGHTTIME_LIGHTS)",
        "description": "Annual cloud-free composites of stable nighttime lights from the Defense Meteorological Satellite Program Operational Linescan System.",
        "variables_available": "avg_vis (average visible band digital number 0-63), cf_cvg (cloud-free coverage count), avg_lights_x_pct (average visible band multiplied by percent frequency)",
        "spatial_resolution": "30 arc-seconds (~1 km at equator)",
        "temporal_coverage": "1992 - 2013 (annual composites)",
        "data_format": "GeoTIFF, Cloud-Optimized GeoTIFF (via GEE)",
        "access_requirements": "Open access; no authentication required for NOAA direct archives or standard Earth Engine API.",
        "licence_restrictions": "Public domain (US Federal Government work); cite NOAA/NCEI Earth Observation Group.",
        "potential_relevance": "Provides the foundational historical baseline of artificial lighting for the first two decades (1992-2012) of the study period.",
        "expected_coverage": "Complete continuous coverage across Bengaluru, Mysuru, and Nilgiri-Bandipur for 1992-2013."
    },
    {
        "category": "A. Nighttime-light / ALAN",
        "dataset_name": "VIIRS-DNB Day/Night Band Monthly/Annual Composites (EOG / NOAA)",
        "official_url": "https://eogdata.mines.edu/products/vnl/ (also via GEE: NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG)",
        "description": "Earth Observation Group (Payne Institute / Colorado School of Mines) suite of monthly and annual nightlight composites filtering ephemeral lights and stray light.",
        "variables_available": "avg_rad (average DNB radiance in nW/cm^2/sr), cf_cvg (cloud-free coverages count)",
        "spatial_resolution": "15 arc-seconds (~500 m at equator)",
        "temporal_coverage": "2012 - 2024 (monthly and annual)",
        "data_format": "GeoTIFF, Cloud-Optimized GeoTIFF",
        "access_requirements": "Open access; free registration required on EOG portal; accessible via Google Earth Engine.",
        "licence_restrictions": "Creative Commons Attribution 4.0 International (CC BY 4.0); attribution to Colorado School of Mines EOG.",
        "potential_relevance": "High dynamic range radiometric measurements without sensor saturation; essential for tracking modern urban light expansion and forest fringe encroachment.",
        "expected_coverage": "Complete coverage across all 3 regions from April 2012 to present. Cloud masking impacts monsoon months (June-September)."
    },
    {
        "category": "A. Nighttime-light / ALAN",
        "dataset_name": "NASA Black Marble (VNP46A2 / VNP46A3 / VNP46A4)",
        "official_url": "https://blackmarble.gsfc.nasa.gov/ and https://ladsweb.modaps.eosdis.nasa.gov/",
        "description": "NASA suite of daily (VNP46A2), monthly (VNP46A3), and annual (VNP46A4) nighttime lights corrected for lunar irradiance, aerosol scattering, atmospheric absorption, and BRDF.",
        "variables_available": "DNB_BRDF-Corrected_NTL (radiance in nW/cm^2/sr), Mandatory_Quality_Flag, Snow_Flag, Moon_Illumination_Fraction",
        "spatial_resolution": "15 arc-seconds (~500 m at equator, 7.5 arc-sec in VNP46 suite)",
        "temporal_coverage": "2012 - 2024 (daily, monthly, annual)",
        "data_format": "HDF5, NetCDF-4, GeoTIFF exports via NASA LAADS DAAC",
        "access_requirements": "Open access; requires free NASA Earthdata login and Bearer token / API authorization.",
        "licence_restrictions": "NASA open data policy (unrestricted worldwide public domain); citation of Roman et al. (2018).",
        "potential_relevance": "Most scientifically rigorous ALAN dataset due to lunar and bidirectional surface reflectance correction; minimizes seasonal vegetation and phase-of-moon noise.",
        "expected_coverage": "Full coverage for Bengaluru, Mysuru, and Nilgiri-Bandipur from 2012 onwards."
    },
    {
        "category": "A. Nighttime-light / ALAN",
        "dataset_name": "Harmonized Global Nighttime Light Dataset (Chen et al. / Li et al.)",
        "official_url": "https://doi.org/10.1038/s41597-020-0510-y (Chen et al. 2021) / https://doi.org/10.5194/essd-12-1951-2020 (Li et al. 2020)",
        "description": "Cross-calibrated, harmonized continuous global nighttime light dataset merging DMSP-OLS and simulated VIIRS-DNB across 1992-2021+.",
        "variables_available": "calibrated_DN (continuous calibrated radiance / digital number index comparable across all 3 decades)",
        "spatial_resolution": "30 arc-seconds (~1 km at equator)",
        "temporal_coverage": "1992 - 2021 (annual)",
        "data_format": "GeoTIFF, available via Figshare / Zenodo / GEE assets",
        "access_requirements": "Open access; direct download from scientific data repositories (Figshare/Zenodo).",
        "licence_restrictions": "Creative Commons Attribution 4.0 International (CC BY 4.0).",
        "potential_relevance": "Solves the inter-sensor calibration gap between DMSP-OLS and VIIRS-DNB; vital for continuous 30-year longitudinal modeling without abrupt 2012-2013 sensor step-changes.",
        "expected_coverage": "Seamless continuous coverage across all 3 study areas for the entire 1992-2021 period."
    },

    # B. Biodiversity Occurrence
    {
        "category": "B. Biodiversity Occurrence",
        "dataset_name": "Global Biodiversity Information Facility (GBIF)",
        "official_url": "https://www.gbif.org/ / https://api.gbif.org/v1/",
        "description": "Global multilateral open-access database aggregating museum specimen records, field surveys, and citizen science observations across all kingdoms of life.",
        "variables_available": "scientificName, decimalLatitude, decimalLongitude, eventDate, year, month, day, coordinateUncertaintyInMeters, basisOfRecord, taxonRank, kingdom, phylum, class, order, family, genus",
        "spatial_resolution": "Point coordinates (uncertainties ranging from 1m to >10km)",
        "temporal_coverage": "Historical (pre-1900) to 2024; high volume post-2010",
        "data_format": "Darwin Core Archive (DwC-A), CSV/TSV, JSON (REST API)",
        "access_requirements": "Open access; requires free GBIF user account to generate citable DOI download requests; REST API allows unauthenticated queries up to rate limits.",
        "licence_restrictions": "CC0 1.0, CC BY 4.0, or CC BY-NC 4.0 depending on data publisher. All project downloads must obtain and cite a unique GBIF DOI.",
        "potential_relevance": "Comprehensive cross-taxa biodiversity database (birds, mammals, lepidoptera, odonata, vascular plants, fungi) required to evaluate multi-trophic responses to ALAN.",
        "expected_coverage": "High density in Bengaluru (urban parks, lakes); moderate in Mysuru; high in Nilgiri-Bandipur (protected area surveys, research camps), but temporal density is heavily skewed post-2012."
    },
    {
        "category": "B. Biodiversity Occurrence",
        "dataset_name": "eBird Basic Dataset (EBD) & eBird API",
        "official_url": "https://ebird.org/science/download-ebird-data / https://documenter.getpostman.com/view/664302/S1ENwy59 (eBird API 2.0)",
        "description": "Semi-structured global citizen science bird observation database managed by the Cornell Lab of Ornithology and Bird Count India.",
        "variables_available": "COMMON NAME, SCIENTIFIC NAME, OBSERVATION COUNT, STATE, COUNTY, LOCALITY, LATITUDE, LONGITUDE, OBSERVATION DATE, TIME OBSERVATIONS STARTED, SAMPLING EVENT IDENTIFIER, PROTOCOL TYPE, DURATION MINUTES, EFFORT DISTANCE KM, ALL SPECIES REPORTED",
        "spatial_resolution": "Point localities / transects (coordinate precision typically 10-100m)",
        "temporal_coverage": "Systematic high volume 2014-2024; sparser historical records 2000-2013",
        "data_format": "Tab-delimited text (.txt / .csv), JSON via REST API",
        "access_requirements": "Requires free eBird account and explicit academic data access request form (approval usually granted within 24-48 hours for academic research); API key available instantly via eBird account.",
        "licence_restrictions": "eBird Terms of Use; academic research non-commercial permitted with full citation of Cornell Lab / Bird Count India.",
        "potential_relevance": "Highest-volume temporal biodiversity time series in Southern India; complete checklists allow computation of reporting rate, presence-absence, and detectability models.",
        "expected_coverage": "Extremely dense in Bengaluru (hundreds of active birders, weekly lake surveys); moderate-high in Mysuru (KRS, Chamundi, Ranganathittu); high in Bandipur-Mudumalai (ecotourism safaris, forest edge)."
    },
    {
        "category": "B. Biodiversity Occurrence",
        "dataset_name": "iNaturalist Research-Grade Observations",
        "official_url": "https://www.inaturalist.org/ / https://api.inaturalist.org/v1/",
        "description": "Community science platform for recording photo- and audio-vouched observations of wild organisms with community taxonomic verification.",
        "variables_available": "id, observed_on, quality_grade, latitude, longitude, positional_accuracy, taxon_name, iconic_taxon_name, num_identification_agreements, photo_url",
        "spatial_resolution": "Point coordinates (research-grade precision typically <100m; obscured to ~10-25km for threatened species)",
        "temporal_coverage": "2010 - 2024 (massive exponential increase after 2016)",
        "data_format": "CSV, JSON via REST API, DwC-A export via GBIF",
        "access_requirements": "Open access; no auth needed for public REST API; export downloads require free registered account.",
        "licence_restrictions": "CC0, CC BY, or CC BY-NC based on observer preference.",
        "potential_relevance": "Critical source for non-avian taxa: nocturnal insects (moths, mantises, beetles), amphibians, reptiles, and nocturnal mammals attracted or repelled by lights.",
        "expected_coverage": "Very high in Bengaluru urban gardens and campuses; moderate in Mysuru; moderate-low within Bandipur core (camera bans / forest regulations) but good on fringes (Masinagudi, Gundlupet)."
    },

    # C. Ecological Interactions / Food Webs
    {
        "category": "C. Ecological Interactions & Food Webs",
        "dataset_name": "Global Biotic Interactions (GloBI)",
        "official_url": "https://www.globalbioticinteractions.org/ / https://api.globalbioticinteractions.org/",
        "description": "Open infrastructure providing programmatic access to curated species interaction data (predation, pollination, parasitism, herbivory) synthesized from scientific literature and natural history collections.",
        "variables_available": "source_taxon_name, target_taxon_name, interaction_type (preysOn, pollinates, eats, parasiteOf, hostOf), interaction_type_id, citation, decimalLatitude, decimalLongitude",
        "spatial_resolution": "Taxon-level network graph; subset of records contain geographic coordinates",
        "temporal_coverage": "Static literature compilation spanning historical to modern publications (undated to present)",
        "data_format": "TSV, CSV, JSON, RDF / Turtle, Cypher graph exports",
        "access_requirements": "Open access; no registration or API key required.",
        "licence_restrictions": "Open Data (CC0 1.0 Universal / Public Domain Dedication).",
        "potential_relevance": "Essential backbone for constructing trophic graphs and interaction networks between observed species in the study landscapes.",
        "expected_coverage": "Broad taxon coverage for Southern Indian species; interaction presence inferred from regional taxonomic checklist overlaps."
    },
    {
        "category": "C. Ecological Interactions & Food Webs",
        "dataset_name": "Mangal (mangal.io)",
        "official_url": "https://mangal.io/ / https://api.mangal.io/api/v2/",
        "description": "Curated database and API for ecological network data, including food webs, host-parasite networks, and mutualistic interaction networks.",
        "variables_available": "network_id, dataset_name, taxon_from, taxon_to, interaction_type, network_topology, geographic_location",
        "spatial_resolution": "Site-specific ecological networks; point or bounding box coordinates",
        "temporal_coverage": "Static archive of published ecological networks (1970s - present)",
        "data_format": "JSON REST API, Julia (Mangal.jl), R (rmangal)",
        "access_requirements": "Open access; open REST API.",
        "licence_restrictions": "Creative Commons Attribution 4.0 International (CC BY 4.0).",
        "potential_relevance": "Provides topological benchmarks (trophic levels, connectance, modularity) for regional food web graphs.",
        "expected_coverage": "Limited direct networks sampled specifically inside Bengaluru/Mysuru; multiple tropical forest food webs applicable to Western Ghats/Nilgiris."
    },
    {
        "category": "C. Ecological Interactions & Food Webs",
        "dataset_name": "Published Indian Ecological Interaction Datasets (ATREE / IISc CES / WII)",
        "official_url": "https://atree.org/ / http://ces.iisc.ac.in/ / https://wii.gov.in/ (Institutional data archives, Shodhganga, Zenodo)",
        "description": "Field-sampled interaction networks from South Indian studies: plant-pollinator networks in urban/rural gradients, herbivore-carnivore trophic interactions in Bandipur-Mudumalai.",
        "variables_available": "Dietary composition (scat analysis data), pollinator visitation matrices, seed dispersal networks, nocturnal flower-moth visitation rates",
        "spatial_resolution": "Field plot scale (local sites across Bandipur, Mudumalai, Bangalore University, GKVK campus)",
        "temporal_coverage": "Study-specific (1988 - 2023)",
        "data_format": "CSV, PDF supplementary tables, Zenodo/Dryad data packages",
        "access_requirements": "Published scientific papers and repositories; mostly open access or accessible via institutional library; requires manual transcription and harmonization.",
        "licence_restrictions": "Academic use with citation of specific publications (e.g. Johnsingh 1992, Karanth & Sunquist 1995, Devy & Davidar 2003, Sinu et al.).",
        "potential_relevance": "Ground-truthing regional interactions: predator-prey ratios (tiger/leopard/dhole/chital) in Bandipur and urban plant-pollinator networks in Bengaluru.",
        "expected_coverage": "High specific relevance for Nilgiri-Bandipur and Bengaluru; sparse for Mysuru."
    },

    # D. Species Traits
    {
        "category": "D. Species Functional Traits",
        "dataset_name": "EltonTraits 1.0 (Global Bird and Mammal Traits)",
        "official_url": "https://doi.org/10.1890/13-1917.1 (Ecology 95:2027, Wilman et al. 2014)",
        "description": "Global comprehensive species-level functional trait database for all 9,993 extant bird species and 5,400 mammal species.",
        "variables_available": "SpecRecID, Scientific, Diet-Inv, Diet-Vend, Diet-Vect, Diet-Fish, Diet-Unk, Diet-Fruit, Diet-Nect, Diet-Seed, Diet-PlantO, ForStrat-watbelowsurf, ForStrat-wataroundsurf, ForStrat-ground, ForStrat-understory, ForStrat-midhigh, ForStrat-canopy, ForStrat-aerial, PelagicSpecialist, Nocturnal, BodyMass-Value",
        "spatial_resolution": "Species-level global attribute (non-spatial table; joinable on scientificName)",
        "temporal_coverage": "Static contemporary synthesis (published 2014, applicable across study window)",
        "data_format": "TXT / CSV / Excel (Ecological Archives E095-178-D1)",
        "access_requirements": "Open access; downloadable directly from Wiley / ESA Ecological Archives or figshare.",
        "licence_restrictions": "Public domain / Open science reuse with attribution (Wilman et al. 2014).",
        "potential_relevance": "Critical predictor for ALAN susceptibility: contains the binary `Nocturnal` trait flag, vertical foraging stratum, and diet proportions for all regional birds and mammals.",
        "expected_coverage": "100% taxonomic coverage for all bird and mammal species recorded across Bengaluru, Mysuru, and Nilgiri-Bandipur."
    },
    {
        "category": "D. Species Functional Traits",
        "dataset_name": "AVONET: Morphological, Functional and Ecological Data on Global Birds",
        "official_url": "https://doi.org/10.1111/ele.13898 (Ecology Letters, Tobias et al. 2022) / Figshare",
        "description": "Comprehensive global functional trait database containing standardized morphological measurements and ecological traits for 11,009 bird species.",
        "variables_available": "Species1, Family1, Order1, Beak.Length_Culmen, Beak.Length_Nares, Beak.Width, Beak.Depth, Tarsus.Length, Wing.Length, Kipps.Distance, Hand-Wing.Index (dispersal capacity), Tail.Length, Mass, Primary.Lifestyle, Habitat, Trophic.Level, Trophic.Niche",
        "spatial_resolution": "Species-level attribute table (joinable on taxonomic names)",
        "temporal_coverage": "Static contemporary synthesis (published 2022)",
        "data_format": "CSV, Excel (Figshare repository)",
        "access_requirements": "Open access; direct download from Figshare / Ecology Letters repository.",
        "licence_restrictions": "CC BY 4.0 International.",
        "potential_relevance": "Provides Hand-Wing Index (dispersal ability to cross brightly lit roads/corridors) and precise trophic niche/morphology for all regional avian species.",
        "expected_coverage": "Complete coverage (>99.5%) for all bird species occurring in Karnataka and Tamil Nadu study sites."
    },
    {
        "category": "D. Species Functional Traits",
        "dataset_name": "PanTHERIA: A Species-Level Database of Life History, Ecology, and Geography of Extant and Recently Extinct Mammals",
        "official_url": "https://doi.org/10.1890/08-1494.1 (Ecology 90:2648, Jones et al. 2009)",
        "description": "Global database of 25 life-history, physiological, ecological, and behavioral traits for 5,416 mammal species.",
        "variables_available": "MSW05_Binomial, ActivityCycle (1=nocturnal, 2=cathemeral, 3=diurnal), AdultBodyMass_g, BasalMetabolicRate_mLO2hr, DietBreadth, HomeRange_km2, LitterSize, PopulationDensity_n/km2, TrophicLevel",
        "spatial_resolution": "Species-level attribute table",
        "temporal_coverage": "Static compilation (published 2009)",
        "data_format": "TXT / CSV (ESA Ecological Archives E090-184)",
        "access_requirements": "Open access; direct download from ESA repository / Ecological Archives.",
        "licence_restrictions": "Public domain / Open science reuse with attribution (Jones et al. 2009).",
        "potential_relevance": "Essential source for mammal activity cycle (diel timing: nocturnal vs cathemeral vs diurnal), home range size, and trophic classification.",
        "expected_coverage": "Complete coverage for all carnivores, herbivores, rodents, and bats recorded in Bandipur-Mudumalai and peri-urban habitats."
    },
    {
        "category": "D. Species Functional Traits",
        "dataset_name": "AmphiBIO: A Global Database for Amphibian Ecological Traits",
        "official_url": "https://doi.org/10.1038/sdata.2017.123 (Nature Scientific Data, Oliveira et al. 2017)",
        "description": "Comprehensive functional trait database for 6,776 amphibian species (anurans, salamanders, caecilians).",
        "variables_available": "Species, Order, Family, Genus, Fos (fossorial), Ter (terrestrial), Aqu (aquatic), Arb (arboreal), Diel_activity (nocturnal, diurnal, both), Body_size_mm, Breeding_strategy",
        "spatial_resolution": "Species-level attribute table",
        "temporal_coverage": "Static compilation (published 2017)",
        "data_format": "CSV, Excel (Nature Scientific Data / Figshare)",
        "access_requirements": "Open access; direct download from Figshare.",
        "licence_restrictions": "Creative Commons Attribution 4.0 International (CC BY 4.0).",
        "potential_relevance": "Amphibians are extraordinarily light-sensitive (melatonin suppression, mating call disruption); AmphiBIO provides microhabitat and nocturnal activity classifications.",
        "expected_coverage": "Covers Western Ghats and Deccan amphibian fauna occurring across our 3 landscapes."
    },

    # E. Environmental Variables
    {
        "category": "E. Environmental Variables",
        "dataset_name": "ESA WorldCover 10m",
        "official_url": "https://esa-worldcover.org/en / https://worldcover2021.esa.int/ (GEE: ESA/WorldCover/v100 and v200)",
        "description": "Global land cover map at 10m spatial resolution based on Sentinel-1 and Sentinel-2 satellite data.",
        "variables_available": "Map (Discrete land cover classes: 10=Tree cover, 20=Shrubland, 30=Grassland, 40=Cropland, 50=Built-up, 60=Bare/sparse vegetation, 80=Permanent water bodies, 90=Herbaceous wetland, 95=Mangroves, 100=Moss/lichen)",
        "spatial_resolution": "10 meters",
        "temporal_coverage": "2020 (v100) and 2021 (v200)",
        "data_format": "Cloud-Optimized GeoTIFF (COG), GEE ImageCollection",
        "access_requirements": "Open access; direct download via ESA WorldCover portal or GEE (no cost).",
        "licence_restrictions": "Creative Commons Attribution 4.0 International (CC BY 4.0); European Space Agency.",
        "potential_relevance": "Highest resolution baseline for mapping built-up surface area, tree canopy cover, water bodies, and agricultural fractions inside each 5km x 5km grid cell.",
        "expected_coverage": "100% complete coverage across Bengaluru, Mysuru, and Nilgiri-Bandipur."
    },
    {
        "category": "E. Environmental Variables",
        "dataset_name": "Hansen Global Forest Change (UMD / Hansen et al.)",
        "official_url": "https://glad.earthengine.app/view/global-forest-change / https://earthenginepartners.appspot.com/science-2013-global-forest-change",
        "description": "Global 30m resolution multi-year analysis of forest extent, annual tree canopy loss, and cumulative forest gain based on Landsat time series.",
        "variables_available": "treecover2000 (0-100% canopy density), loss (0 or 1), gain (0 or 1), lossyear (year of forest loss 1-23 = 2001-2023), datamask",
        "spatial_resolution": "30 meters (1 arc-second)",
        "temporal_coverage": "2000 - 2023 (annual updates)",
        "data_format": "GeoTIFF tiles, Google Earth Engine asset (UMD/hansen/global_forest_change_2023_v1_11)",
        "access_requirements": "Open access; direct HTTP download of 10x10 degree tiles or GEE access.",
        "licence_restrictions": "Attribution to Hansen et al. (2013) Science; CC BY 4.0.",
        "potential_relevance": "Direct measure of forest fragmentation, degradation, and deforestation over the last 24 years; critical for tracking canopy changes along the Bandipur-Mudumalai highway corridors.",
        "expected_coverage": "100% complete coverage for all three study regions."
    },
    {
        "category": "E. Environmental Variables",
        "dataset_name": "WorldPop Gridded Population Count and Density",
        "official_url": "https://www.worldpop.org/ / https://hub.worldpop.org/geodata/listing?id=29",
        "description": "High-resolution annual gridded estimates of human population count and population density (people per km² / pixel).",
        "variables_available": "population_count, population_density (unconstrained and constrained individual countries)",
        "spatial_resolution": "3 arc-seconds (~100 meters at equator)",
        "temporal_coverage": "2000 - 2020 (annual)",
        "data_format": "GeoTIFF, Cloud-Optimized GeoTIFF, GEE (WorldPop/GP/100m/pop)",
        "access_requirements": "Open access; direct download from WorldPop repository.",
        "licence_restrictions": "Creative Commons Attribution 4.0 International (CC BY 4.0).",
        "potential_relevance": "Provides direct measure of human population pressure to decouple lighting effects from population density in statistical and neural models.",
        "expected_coverage": "Complete continuous annual coverage for Bengaluru, Mysuru, and Nilgiri-Bandipur (2000-2020)."
    },
    {
        "category": "E. Environmental Variables",
        "dataset_name": "Global Human Settlement Layer (GHSL - JRC)",
        "official_url": "https://ghsl.jrc.ec.europa.eu/ / https://ghsl.jrc.ec.europa.eu/download.php",
        "description": "European Commission Joint Research Centre multi-temporal spatial data on human presence on the planet: built-up surface area (GHS-BUILT-S) and settlement characteristics.",
        "variables_available": "built_surface_m2, built_volume_m3, settlement_grid (urban centre, dense urban cluster, semi-dense cluster, suburban, rural)",
        "spatial_resolution": "100m, 1km, and multiscale tiles",
        "temporal_coverage": "Epochs: 1975, 1990, 2000, 2015, 2020, 2025 (5-year / multiannual epochs)",
        "data_format": "GeoTIFF (Mollweide and WGS84 projections)",
        "access_requirements": "Open access; direct download from JRC open portal.",
        "licence_restrictions": "European Commission open data policy (reuse allowed with attribution).",
        "potential_relevance": "Provides long-term physical infrastructure expansion data spanning the full 1992-2024 period, enabling decoupling of built structures from luminaire illumination.",
        "expected_coverage": "Complete spatial coverage across all 3 regions for all standard epochs."
    },
    {
        "category": "E. Environmental Variables",
        "dataset_name": "ERA5-Land Hourly and Monthly Gridded Climate Reanalysis",
        "official_url": "https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land (Copernicus Climate Data Store)",
        "description": "Enhanced global atmospheric and surface reanalysis produced by ECMWF providing continuous land surface climate variables.",
        "variables_available": "2m_temperature, 2m_dewpoint_temperature, total_precipitation, surface_solar_radiation_downwards, volumetric_soil_water_layer_1, surface_sensible_heat_flux",
        "spatial_resolution": "0.1° x 0.1° (~9 km resolution)",
        "temporal_coverage": "1950 - present (continuous hourly and monthly)",
        "data_format": "GRIB, NetCDF-4",
        "access_requirements": "Open access; requires free Copernicus CDS account, API key, and agreement to terms of use; programmatic download via `cdsapi` Python client.",
        "licence_restrictions": "Copernicus licence; free and open reuse with citation of ECMWF / Copernicus.",
        "potential_relevance": "Essential environmental covariates: controls for seasonal and climatic drivers of animal phenology, temperature anomalies, cloudiness, and rainfall.",
        "expected_coverage": "Complete uninterrupted hourly and monthly time series (1992-2024) across all 3 regions."
    },
    {
        "category": "E. Environmental Variables",
        "dataset_name": "Copernicus Global Digital Elevation Model (GLO-30)",
        "official_url": "https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model / https://registry.opendata.aws/copernicus-dem/",
        "description": "High-accuracy global digital surface model (DSM) derived from TanDEM-X satellite radar interferometry.",
        "variables_available": "elevation (meters above sea level), derived slope (degrees), derived aspect, topographic position index (TPI), terrain ruggedness index (TRI)",
        "spatial_resolution": "30 meters (1 arc-second)",
        "temporal_coverage": "Static contemporary acquisition (2011-2015 radar acquisitions, published 2021)",
        "data_format": "Cloud-Optimized GeoTIFF (COG), available via AWS S3 open bucket and Planetary Computer",
        "access_requirements": "Open access; no auth needed on AWS S3 open bucket (`s3://copernicus-dem-30m/`) or MS Planetary Computer.",
        "licence_restrictions": "Free and open data policy; attribution to Airbus / European Space Agency.",
        "potential_relevance": "Critical topographic control: elevation ranges from ~600m in Mysuru/Moyar gorge up to ~1,500m+ in Nilgiri escarpment; controls light propagation, skyglow trapping, and montane species distributions.",
        "expected_coverage": "100% complete coverage with zero data voids across all three study areas."
    },
    {
        "category": "E. Environmental Variables",
        "dataset_name": "OpenStreetMap (OSM) Infrastructure & Lighting Vectors",
        "official_url": "https://www.openstreetmap.org/ / https://download.geofabrik.de/asia/india.html / Overpass API",
        "description": "Global collaborative geospatial database of roads, highways, building footprints, land use, and street lighting tags (`lit=yes/no`).",
        "variables_available": "highway (motorway, trunk, primary, secondary, residential), lit (yes, no, 24/7, sunset-sunrise), lamp_type, building, landuse, amenity",
        "spatial_resolution": "Vector geometry (meter-level accuracy)",
        "temporal_coverage": "Current snapshot + full historical edit history via OSM History Database (OSHDB)",
        "data_format": "OSM PBF (.osm.pbf), GeoJSON, Shapefile via Geofabrik",
        "access_requirements": "Open access; direct download of regional extracts (Karnataka, Tamil Nadu) or Overpass API queries.",
        "licence_restrictions": "Open Database License (ODbL 1.0); requires OpenStreetMap contributor attribution.",
        "potential_relevance": "Provides exact vectors of highway networks (NH-766, NH-181 passing through Bandipur/Mudumalai), street lighting tags in Bengaluru/Mysuru, and human physical infrastructure density.",
        "expected_coverage": "Road network is 99% complete in all 3 regions; specific `lit=*` tags are dense in central Bengaluru, moderate in Mysuru, and sparse in rural/forest roads."
    },
    {
        "category": "E. Environmental Variables",
        "dataset_name": "World Database on Protected Areas (WDPA / Protected Planet)",
        "official_url": "https://www.protectedplanet.net/en/the-world-database-on-protected-areas-wdpa",
        "description": "Official global database of terrestrial and marine protected areas compiled by UNEP-WCMC and IUCN.",
        "variables_available": "WDPAID, NAME, DESIG, DESIG_ENG, IUCN_CAT (Ia, Ib, II, IV, etc.), STATUS_YR, GOV_TYPE, REP_AREA, GIS_AREA",
        "spatial_resolution": "Vector polygon boundaries",
        "temporal_coverage": "Current legal boundaries with gazetting years (historical boundary changes tracked via versions)",
        "data_format": "GeoPackage, Shapefile, CSV",
        "access_requirements": "Open access; free direct download for non-commercial educational/scientific research.",
        "licence_restrictions": "UNEP-WCMC terms of use; non-commercial research allowed with citation.",
        "potential_relevance": "Provides authoritative legal boundaries for Bandipur NP (WDPA 862), Mudumalai TR (WDPA 863), Bannerghatta NP (WDPA 860), and Ranganathittu Bird Sanctuary (WDPA 14282).",
        "expected_coverage": "Complete verified coverage for all designated protected areas in the study landscapes."
    },

    # F. Independent Validation
    {
        "category": "F. Independent Validation",
        "dataset_name": "BioTIME Database of Global Biodiversity Time Series",
        "official_url": "https://biotime.st-andrews.ac.uk/ / https://doi.org/10.1111/geb.12729 (Dornelas et al. 2018)",
        "description": "Curated database of biodiversity time series consisting of assemblage surveys with consistent methodology repeated over a minimum of 2 years.",
        "variables_available": "STUDY_ID, PLOT, YEAR, MONTH, DAY, GENUS_SPECIES, ABUNDANCE, BIOMASS, LATITUDE, LONGITUDE",
        "spatial_resolution": "Site / plot specific coordinates",
        "temporal_coverage": "Multi-decadal surveys (varying subsets from 1950 to 2020)",
        "data_format": "CSV, R data package",
        "access_requirements": "Open access; direct download from BioTIME data portal (University of St Andrews).",
        "licence_restrictions": "Creative Commons Attribution 4.0 International (CC BY 4.0).",
        "potential_relevance": "Independent ground-truth validation for temporal population trends, species turnover, and community assemblage stability.",
        "expected_coverage": "Moderate in Western Ghats / Nilgiris region (several forest assemblage time series); no dedicated urban time series for Bengaluru or Mysuru."
    },
    {
        "category": "F. Independent Validation",
        "dataset_name": "PREDICTS: Projecting Responses of Ecological Diversity In Changing Terrestrial Systems",
        "official_url": "https://data.nhm.ac.uk/dataset/predicts-database / https://doi.org/10.5519/0066354 (Hudson et al. 2017)",
        "description": "Global database of site-level species richness and abundance comparisons across contrasting land-use intensities (primary vegetation, secondary vegetation, plantation, cropland, pasture, urban).",
        "variables_available": "Source_ID, Study_name, Site_name, Longitude, Latitude, Predominant_land_use, Use_intensity, Taxon_name, Measurement, Effort_corrected_measurement",
        "spatial_resolution": "Site-level GPS coordinates (typically with positional precision <1 km)",
        "temporal_coverage": "Studies published between 1984 and 2016",
        "data_format": "CSV, R data package",
        "access_requirements": "Open access; downloadable directly from the Natural History Museum Data Portal (London).",
        "licence_restrictions": "CC BY 4.0 International; Natural History Museum London.",
        "potential_relevance": "Empirical validation of biodiversity response functions across land-use gradients; allows testing whether model predicts observed biodiversity suppression along urban edges.",
        "expected_coverage": "Contains multiple studies across the Western Ghats and Southern Indian agricultural/plantation mosaics; provides crucial reference response baselines."
    },
    {
        "category": "F. Independent Validation",
        "dataset_name": "WII All India Tiger & Herbivore Monitoring Survey Reports (NTCA / WII)",
        "official_url": "https://wii.gov.in/status_tigers_co_predators_2022 and https://ntca.gov.in/",
        "description": "Quadrennial national camera-trap and distance sampling surveys across all tiger reserves in India (2006, 2010, 2014, 2018, 2022).",
        "variables_available": "Camera trap encounter rates, individual tiger IDs, leopard encounter rates, distance-sampling herbivore density (chital, sambar, gaur, elephant dung density per km²)",
        "spatial_resolution": "Beat and 2 km x 2 km camera-trap grid level",
        "temporal_coverage": "2006, 2010, 2014, 2018, 2022 (quadrennial reports)",
        "data_format": "Published government reports (PDF), summary tables, WII GIS portal",
        "access_requirements": "Summary reports open access; raw high-resolution camera trap image coordinates require official research permission from NTCA / Karnataka & Tamil Nadu Forest Departments.",
        "licence_restrictions": "Government of India copyright; academic citation of official technical reports.",
        "potential_relevance": "Unrivalled independent benchmark of apex predator and large herbivore abundance and spatial occupancy inside the Bandipur-Mudumalai landscape.",
        "expected_coverage": "Exhaustive for Nilgiri-Bandipur landscape; non-existent for central Bengaluru or urban Mysuru (except Bannerghatta buffer)."
    },
    {
        "category": "F. Independent Validation",
        "dataset_name": "Mudumalai 50-Hectare Permanent Forest Dynamics Plot (IISc CES / ForestGEO)",
        "official_url": "https://forestgeo.si.edu/sites/asia/mudumalai and http://ces.iisc.ac.in/",
        "description": "Continuous, long-term tropical dry deciduous forest dynamics plot established in 1988 in Mudumalai (part of Smithsonian ForestGEO network), tracking survival, growth, and mortality of all woody stems >= 1cm DBH.",
        "variables_available": "Tag_ID, Species, DBH, Coordinates_X, Coordinates_Y, Status (alive/dead), Fire_damage, Elephant_damage",
        "spatial_resolution": "50-hectare continuous plot (20m x 20m subquadrats)",
        "temporal_coverage": "1988 - present (continuous 5-year full censuses: 1988, 1993, 1998, 2003, 2008, 2013, 2018, 2023)",
        "data_format": "Institutional database / ForestGEO data request portal",
        "access_requirements": "Formal data request via ForestGEO portal / direct academic collaboration with IISc Centre for Ecological Sciences (Prof. R. Sukumar group).",
        "licence_restrictions": "ForestGEO data sharing policy / collaborative co-authorship agreement.",
        "potential_relevance": "Gold standard ground-truth validation for 35-year continuous ecological stability in the Nilgiri-Bandipur core forest, proving whether vegetation dynamics are driven by climate, fire, or external pressures.",
        "expected_coverage": "Highly localized to Mudumalai dry deciduous zone inside our Nilgiri-Bandipur study window."
    }
]

REGIONAL_MATRIX = [
    {
        "dataset_name": "DMSP-OLS Nighttime Lights",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "1992 - 2013 (annual)",
        "spatial_resolution": "~1 km (30 arc-sec)",
        "collection_difficulty": "Low (Direct download / GEE)",
        "important_limitations": "Severe digital number saturation in Bengaluru city center (max DN=63); lack of on-board calibration requires inter-satellite normalization; coarse 1km pixel blends forest edges."
    },
    {
        "dataset_name": "VIIRS-DNB Monthly/Annual (EOG)",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "2012 - 2024 (monthly/annual)",
        "spatial_resolution": "~500 m (15 arc-sec)",
        "collection_difficulty": "Low (EOG free account / GEE)",
        "important_limitations": "Monsoon cloud cover causes missing observations in July-September; does not cover pre-2012 historical window; sensitive to viewing angle / ephemeral lighting."
    },
    {
        "dataset_name": "NASA Black Marble (VNP46A2/A3/A4)",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "2012 - 2024 (daily/monthly/annual)",
        "spatial_resolution": "~500 m (15 arc-sec)",
        "collection_difficulty": "Low to Moderate (NASA Earthdata token)",
        "important_limitations": "Starts 2012; large file sizes for daily products; requires HDF5 extraction and projection pipelines."
    },
    {
        "dataset_name": "Harmonized DMSP-VIIRS (Chen/Li)",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "1992 - 2021 (annual continuous)",
        "spatial_resolution": "~1 km (30 arc-sec)",
        "collection_difficulty": "Low (Direct Figshare/Zenodo)",
        "important_limitations": "Model-derived calibration introduces slight smoothing; coarse 1 km resolution limits small habitat patch evaluation; ended in 2021."
    },
    {
        "dataset_name": "GBIF Biodiversity Occurrences",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Sparse pre-2010; dense 2012-2024",
        "spatial_resolution": "Point (1m to >5km)",
        "collection_difficulty": "Low (REST API / DOI export)",
        "important_limitations": "Extreme reporting bias toward road corridors, tourist tracks, and urban botanical gardens; high temporal heterogeneity pre-2010; sensitive species coordinates obscured."
    },
    {
        "dataset_name": "eBird Basic Dataset (EBD)",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Dense 2014-2024; sparse 2000-2013",
        "spatial_resolution": "Point / transect coordinates",
        "collection_difficulty": "Moderate (Data access request approval)",
        "important_limitations": "Taxonomically restricted to birds; observer effort bias towards urban wetlands and famous protected areas; monsoon observer dropout."
    },
    {
        "dataset_name": "iNaturalist Research-Grade",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Limited coverage (core protected area restricted)",
        "historical_coverage": "2015 - 2024 (virtually absent pre-2015)",
        "spatial_resolution": "Point (<100m; obscured for red-list taxa)",
        "collection_difficulty": "Low (API / DwC-A)",
        "important_limitations": "Nilgiri-Bandipur core has limited user observations due to tourist route restrictions; almost no historical depth prior to 2015; smartphone penetration bias."
    },
    {
        "dataset_name": "GloBI Biotic Interactions",
        "bengaluru_availability": "Likely available, needs verification",
        "mysuru_availability": "Likely available, needs verification",
        "nilgiri_bandipur_availability": "Likely available, needs verification",
        "historical_coverage": "Non-temporal (taxonomic network)",
        "spatial_resolution": "Global/Taxon-level network graph",
        "collection_difficulty": "Low (Open REST API / TSV dump)",
        "important_limitations": "Many regional tropical interactions missing from global literature; requires taxonomic name fuzzy matching; spatial context often absent in interaction records."
    },
    {
        "dataset_name": "Mangal Ecological Networks",
        "bengaluru_availability": "Limited coverage",
        "mysuru_availability": "Limited coverage",
        "nilgiri_bandipur_availability": "Likely available, needs verification",
        "historical_coverage": "Non-temporal (archived networks)",
        "spatial_resolution": "Network topology / plot level",
        "collection_difficulty": "Low (REST API / JSON)",
        "important_limitations": "Very few urban food webs archived for Indian subcontinent; predominantly tropical forest and generalist webs; requires network synthesis."
    },
    {
        "dataset_name": "Published Indian Ecological Datasets",
        "bengaluru_availability": "Confirmed available (academic literature)",
        "mysuru_availability": "Limited coverage",
        "nilgiri_bandipur_availability": "Confirmed available (academic literature)",
        "historical_coverage": "1988 - 2023 (study-specific)",
        "spatial_resolution": "Study site / transect level",
        "collection_difficulty": "High (Manual literature curation / contact authors)",
        "important_limitations": "Disparate non-standardized formats (PDF tables, supplementary spreadsheets); requires manual digitisation and harmonization."
    },
    {
        "dataset_name": "EltonTraits 1.0",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Non-temporal (static contemporary)",
        "spatial_resolution": "Species-level attribute table",
        "collection_difficulty": "Low (Direct download)",
        "important_limitations": "Static traits assume fixed species behavior across urban and wild gradients; lacks intraspecific trait plasticity under severe light pollution."
    },
    {
        "dataset_name": "AVONET Functional Traits",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Non-temporal (static contemporary)",
        "spatial_resolution": "Species-level attribute table",
        "collection_difficulty": "Low (Direct Figshare download)",
        "important_limitations": "Restricted to birds; static morphology does not reflect temporal trait shifts."
    },
    {
        "dataset_name": "PanTHERIA Mammal Traits",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Non-temporal (static contemporary)",
        "spatial_resolution": "Species-level attribute table",
        "collection_difficulty": "Low (Direct download)",
        "important_limitations": "Some small mammal / rodent species have missing trait values (data gaps imputable via phylogenetic mean); static."
    },
    {
        "dataset_name": "AmphiBIO Amphibian Traits",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Non-temporal (static contemporary)",
        "spatial_resolution": "Species-level attribute table",
        "collection_difficulty": "Low (Direct Figshare download)",
        "important_limitations": "Cryptic Western Ghats amphibian species splits since 2017 may require taxonomic harmonization."
    },
    {
        "dataset_name": "ESA WorldCover 10m",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "2020 and 2021 only",
        "spatial_resolution": "10 meters",
        "collection_difficulty": "Low (Direct COG download / GEE)",
        "important_limitations": "Only two recent epochs (2020, 2021); cannot track historical land cover changes during the 1990s or 2000s directly without supplementary Landsat/MODIS products."
    },
    {
        "dataset_name": "Hansen Global Forest Change",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "2000 - 2023 (annual)",
        "spatial_resolution": "30 meters",
        "collection_difficulty": "Low (Direct HTTP / GEE)",
        "important_limitations": "Bengaluru and Mysuru urban vegetation (gardens, tree-lined avenues) may be misclassified as plantation or not meet tree height thresholds; forest gain layer is cumulative only."
    },
    {
        "dataset_name": "WorldPop Population Density",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "2000 - 2020 (annual)",
        "spatial_resolution": "~100 meters (3 arc-sec)",
        "collection_difficulty": "Low (Direct download / GEE)",
        "important_limitations": "Modelled disaggregation from subdistrict census figures; may overestimate settlement inside core protected forest enclaves."
    },
    {
        "dataset_name": "GHSL Built-up Surface (JRC)",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "1975, 1990, 2000, 2015, 2020, 2025",
        "spatial_resolution": "100m / 1km",
        "collection_difficulty": "Low (Direct JRC portal)",
        "important_limitations": "Epoch-based (multi-year steps) rather than continuous annual time series; early epochs (1975, 1990) have lower satellite sensor fidelity."
    },
    {
        "dataset_name": "ERA5-Land Climate Reanalysis",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "1950 - present (hourly/monthly)",
        "spatial_resolution": "~9 km (0.1°)",
        "collection_difficulty": "Moderate (Copernicus CDS API queuing)",
        "important_limitations": "Coarse ~9km spatial grid requires spatial downscaling / interpolation across mountainous escarpment topography in Nilgiris."
    },
    {
        "dataset_name": "Copernicus DEM (GLO-30)",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Static contemporary (2011-2015 base)",
        "spatial_resolution": "30 meters",
        "collection_difficulty": "Low (AWS S3 open bucket / Planetary Computer)",
        "important_limitations": "Digital Surface Model (includes canopy top and building elevations rather than bare earth DTM); static over time."
    },
    {
        "dataset_name": "OpenStreetMap Vectors",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Current snapshot complete; historical (2008-2024 via OSHDB)",
        "spatial_resolution": "Meter-scale vectors",
        "collection_difficulty": "Low to Moderate (Geofabrik extract / Overpass API)",
        "important_limitations": "Tag completeness is uneven: `lit=*` street lighting tag is sparse outside central municipal zones; historical changes reflect mapper activity rather than true construction dates."
    },
    {
        "dataset_name": "WDPA Protected Areas",
        "bengaluru_availability": "Confirmed available",
        "mysuru_availability": "Confirmed available",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "Current legal boundaries + gazette year",
        "spatial_resolution": "Vector polygon",
        "collection_difficulty": "Low (Direct Protected Planet download)",
        "important_limitations": "Does not delineate newly declared eco-sensitive zones (ESZ) or minor corridor buffer patches without state gazette notification shapefiles."
    },
    {
        "dataset_name": "BioTIME Database",
        "bengaluru_availability": "Unavailable",
        "mysuru_availability": "Unavailable",
        "nilgiri_bandipur_availability": "Likely available, needs verification",
        "historical_coverage": "Multi-decadal subsets",
        "spatial_resolution": "Plot-level GPS",
        "collection_difficulty": "Low (Direct download)",
        "important_limitations": "No long-term BioTIME plots registered inside Bengaluru or Mysuru urban limits; Western Ghats plots are outside or adjacent to Bandipur boundary."
    },
    {
        "dataset_name": "PREDICTS Database",
        "bengaluru_availability": "Limited coverage",
        "mysuru_availability": "Limited coverage",
        "nilgiri_bandipur_availability": "Confirmed available",
        "historical_coverage": "1984 - 2016 (study-specific snapshots)",
        "spatial_resolution": "Site-level GPS",
        "collection_difficulty": "Low (Direct download)",
        "important_limitations": "Snapshots rather than continuous longitudinal time series; primarily useful for validating static response curves across land use categories."
    },
    {
        "dataset_name": "WII All India Tiger Monitoring",
        "bengaluru_availability": "Unavailable (except Bannerghatta fringe)",
        "mysuru_availability": "Unavailable",
        "nilgiri_bandipur_availability": "Confirmed available (Technical Reports)",
        "historical_coverage": "2006, 2010, 2014, 2018, 2022 (quadrennial)",
        "spatial_resolution": "2 km x 2 km camera-trap grid / beat level",
        "collection_difficulty": "High for raw microdata; Moderate for published report summaries",
        "important_limitations": "Raw camera trap coordinates and photo records are legally classified as restricted government data under NTCA guidelines; report-level metrics are available."
    },
    {
        "dataset_name": "Mudumalai 50-ha Forest Dynamics Plot",
        "bengaluru_availability": "Unavailable",
        "mysuru_availability": "Unavailable",
        "nilgiri_bandipur_availability": "Confirmed available (ForestGEO / IISc CES)",
        "historical_coverage": "1988 - present (5-year census intervals)",
        "spatial_resolution": "Subquadrat (20m x 20m) inside 50-ha plot",
        "collection_difficulty": "High (Requires formal academic collaboration / ForestGEO proposal)",
        "important_limitations": "Restricted to one contiguous 50-hectare site inside Mudumalai; vegetation-only (woody plants >= 1cm DBH), no direct faunal censuses."
    }
]

def export_csvs():
    # Export dataset inventory CSV
    paths_inventory = [
        "dark_eco/dataset_inventory.csv",
        "dark_eco/reports/dataset_inventory/dataset_inventory.csv"
    ]
    inv_headers = [
        "category", "dataset_name", "official_url", "description",
        "variables_available", "spatial_resolution", "temporal_coverage",
        "data_format", "access_requirements", "licence_restrictions",
        "potential_relevance", "expected_coverage"
    ]
    for p in paths_inventory:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=inv_headers)
            writer.writeheader()
            writer.writerows(INVENTORY_DATA)
        print(f"Written: {p} ({len(INVENTORY_DATA)} datasets)")

    # Export regional availability matrix CSV
    paths_matrix = [
        "dark_eco/regional_availability_matrix.csv",
        "dark_eco/reports/dataset_inventory/regional_availability_matrix.csv"
    ]
    mat_headers = [
        "dataset_name", "bengaluru_availability", "mysuru_availability",
        "nilgiri_bandipur_availability", "historical_coverage",
        "spatial_resolution", "collection_difficulty", "important_limitations"
    ]
    for p in paths_matrix:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=mat_headers)
            writer.writeheader()
            writer.writerows(REGIONAL_MATRIX)
        print(f"Written: {p} ({len(REGIONAL_MATRIX)} entries)")

if __name__ == "__main__":
    export_csvs()

