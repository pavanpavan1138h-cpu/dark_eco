# Dark Ecology Intelligence (DEI) — Phase 3: Biodiversity Occurrences
# GBIF DOWNLOAD EXECUTION & PROVENANCE REPORT

**Project**: Dark Ecology Intelligence (DEI) — Artificial Neural Networks Problem-Based Learning (ANN PBL)  
**Execution Date**: November 2026  
**Status**: **DOWNLOAD COMPLETED & VERIFIED**  
**Governing Rule**: Strict Evidence-Based Assessment | Zero Synthetic Data | No Git Push  

---

## 1. Executive Summary

Formal user authorization was received to execute the validated GBIF registered occurrence download for Phase 3. The request was authenticated using credentials stored securely in `dark_eco/.env`, submitted to the official GBIF Asynchronous Occurrence Download API, monitored to completion, downloaded via an atomic `.part` transfer, verified with SHA-256 hashing, and extracted into the designated raw data archive.

The download produced **exactly 3,901,020 occurrence records**, perfectly matching the pre-submission expected count across all three study landscapes with **zero discrepancy**.

---

## 2. GBIF Download Registration & Metadata

```
GBIF Download Registration Summary:
========================================================================================
Parameter                  Value / Status
----------------------------------------------------------------------------------------
Download Identifier        0025038-261023074918325
Official Citable DOI       https://doi.org/10.15468/dl.rum47g (10.15468/dl.rum47g)
Format                     DWCA (Darwin Core Archive)
License                    CC BY-NC 4.0 / CC BY 4.0 / CC0
Submission Timestamp       2026-11-03T15:49:20Z
Completion Timestamp       2026-11-03T17:16:11Z (Status: SUCCEEDED)
Download URL               https://api.gbif.org/v1/occurrence/download/request/0025038-261023074918325.zip
Archive Filename           gbif_dei_2012_2024_three_landscapes_dwca.zip
Archive Size (Compressed)  1,165,036,032 bytes (1,165.0 MB / 1.165 GB)
SHA-256 Checksum           10621204417a59709ad931ecaecfed0cc87c017f64e142d0186d0cfccae68038
Total Record Count         3,901,020 (Expected: 3,901,020; Delta: 0)
========================================================================================
```

---

## 3. Submitted Download Predicate Architecture

The registered download was submitted using the approved predicate structure with no modifications:

```json
{
  "creator": "<gbif_username>",
  "notificationAddresses": ["<user_email>"],
  "sendNotification": true,
  "format": "DWCA",
  "predicate": {
    "type": "and",
    "predicates": [
      {
        "type": "greaterThanOrEquals",
        "key": "YEAR",
        "value": "2012"
      },
      {
        "type": "lessThanOrEquals",
        "key": "YEAR",
        "value": "2024"
      },
      {
        "type": "equals",
        "key": "HAS_COORDINATE",
        "value": "true"
      },
      {
        "type": "equals",
        "key": "HAS_GEOSPATIAL_ISSUE",
        "value": "false"
      },
      {
        "type": "or",
        "predicates": [
          {
            "type": "within",
            "geometry": "POLYGON ((77.817859 12.739603, 77.822948 13.191189, 77.361986 13.195857, 77.357725 12.744105, 77.817859 12.739603))"
          },
          {
            "type": "within",
            "geometry": "POLYGON ((76.883407 12.079049, 76.886631 12.530962, 76.426593 12.533799, 76.424155 12.081780, 76.883407 12.079049))"
          },
          {
            "type": "within",
            "geometry": "POLYGON ((76.824013 11.428614, 76.826965 11.880564, 76.368036 11.883159, 76.365825 11.431108, 76.824013 11.428614))"
          }
        ]
      }
    ]
  }
}
```

*Note: In accordance with credential security rules, credentials were injected dynamically at runtime via HTTP Basic Authentication headers directly from `dark_eco/.env`. No credentials or emails appear in version control, logs, or reports.*

---

## 4. Download Execution Lifecycle

1. **Submission**: Sent to `https://api.gbif.org/v1/occurrence/download/request` at `2026-11-03T15:49:20Z`. GBIF acknowledged with HTTP 201 Created and assigned identifier `0025038-261023074918325`.
2. **Cluster Processing**: 
   - `[0s]` Status: `PREPARING`
   - `[1572s]` Status: `RUNNING`
   - `[5211s]` Status: `SUCCEEDED`
   - Total cluster processing time: ~86 minutes.
3. **Download Transfer**:
   - Downloaded to `data/raw/gbif/gbif_dei_2012_2024_three_landscapes_dwca.zip.part`.
   - Transfer rate: 16.5 MB/s average (completed in ~71 seconds).
   - Atomic rename to `gbif_dei_2012_2024_three_landscapes_dwca.zip`.
4. **Integrity & Checksum**:
   - Local SHA-256 recalculated: `10621204417a59709ad931ecaecfed0cc87c017f64e142d0186d0cfccae68038`.
   - File size verified: exactly `1,165,036,032 bytes`.
5. **Extraction**:
   - Extracted into `data/raw/gbif/extracted/`.
   - Contains `meta.xml`, `metadata.xml`, `citations.txt`, `rights.txt`, `occurrence.txt` (4.57 GB), `verbatim.txt` (2.24 GB), `multimedia.txt` (32.3 MB), and 90 dataset metadata descriptors.

---

## 5. Regional Record Count Verification

```
Empirical Record Count Reconciliation Matrix:
========================================================================================================
Landscape                Expected Clean Count    Actual Archive Count    Delta     Status
--------------------------------------------------------------------------------------------------------
Bengaluru (Urban)              2,947,292               2,947,292           0       EXACT RECONCILIATION
Mysuru (Peri-Urban)              761,890                 761,890           0       EXACT RECONCILIATION
Nilgiri-Bandipur (Forest)        191,838                 191,838           0       EXACT RECONCILIATION
--------------------------------------------------------------------------------------------------------
COMBINED ARCHIVE               3,901,020               3,901,020           0       CERTIFIED COMPLETE
========================================================================================================
```

---

## 6. Security and Compliance Audit

1. **Zero Credential Leaks**: Credentials were accepted exclusively through local configuration (`.env`). No passwords, authentication tokens, or personal emails were output in chat, logs, or documentation.
2. **`.gitignore` Enforcement**: Verified that `data/raw/gbif/**`, `*.zip`, `*.txt`, and `.env` are strictly excluded from git tracking.
3. **No Git Push**: Repository remains strictly local.
4. **Frozen Research Scope**: Only GBIF occurrences have been retrieved. No data acquisition for GloBI or ESA WorldCover has been initiated.

---

## 7. Deliverable Status

- **Archive File**: `dark_eco/data/raw/gbif/gbif_dei_2012_2024_three_landscapes_dwca.zip`
- **Extracted Directory**: `dark_eco/data/raw/gbif/extracted/`
- **Manifest File**: `dark_eco/data/metadata/gbif_download_manifest.json`
- **Summary Statistics**: `dark_eco/data/metadata/gbif_archive_integrity_summary.json`
- **Execution Script**: `dark_eco/scripts/phase_3_biodiversity/execute_gbif_download.py`

