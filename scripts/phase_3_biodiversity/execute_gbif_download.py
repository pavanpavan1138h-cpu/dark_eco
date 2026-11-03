#!/usr/bin/env python3
"""
Dark Ecology Intelligence (DEI) — Phase 3
Script: execute_gbif_download.py

Submits, monitors, downloads, and audits the approved GBIF DWCA occurrence archive
for the three study landscapes (Bengaluru, Mysuru, Nilgiri-Bandipur) 2012-2024.

Strict Rules:
- Never print or leak passwords, emails, or auth headers.
- Credentials read securely from dark_eco/.env or environment variables.
- Verified predicate matching the approved research scope.
"""

import os
import sys
import json
import time
import hashlib
import zipfile
import urllib.request
import urllib.error
import base64

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
RAW_GBIF_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "gbif")
METADATA_DIR = os.path.join(PROJECT_ROOT, "data", "metadata")
MANIFEST_PATH = os.path.join(METADATA_DIR, "gbif_download_manifest.json")

# Verified WKT geometries
WKT_BLR = "POLYGON ((77.817859 12.739603, 77.822948 13.191189, 77.361986 13.195857, 77.357725 12.744105, 77.817859 12.739603))"
WKT_MYS = "POLYGON ((76.883407 12.079049, 76.886631 12.530962, 76.426593 12.533799, 76.424155 12.081780, 76.883407 12.079049))"
WKT_NB  = "POLYGON ((76.824013 11.428614, 76.826965 11.880564, 76.368036 11.883159, 76.365825 11.431108, 76.824013 11.428614))"

def load_credentials():
    """Load credentials from .env or environment securely without echoing secrets."""
    creds = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    creds[k.strip()] = v.strip().strip('"').strip("'")
                    
    # Environment variables take precedence if set
    for k in ["GBIF_USER", "GBIF_PWD", "GBIF_EMAIL"]:
        if k in os.environ:
            creds[k] = os.environ[k]
            
    return creds

def check_credentials():
    creds = load_credentials()
    user_ok = bool(creds.get("GBIF_USER"))
    pwd_ok = bool(creds.get("GBIF_PWD"))
    email_ok = bool(creds.get("GBIF_EMAIL"))
    
    print("--- GBIF Credential Configuration Check ---")
    print(f"  GBIF_USER: {'CONFIGURED' if user_ok else 'MISSING'}")
    print(f"  GBIF_PWD:  {'CONFIGURED' if pwd_ok else 'MISSING'}")
    print(f"  GBIF_EMAIL:{'CONFIGURED' if email_ok else 'MISSING'}")
    return user_ok and pwd_ok and email_ok

def build_predicate():
    return {
        "type": "and",
        "predicates": [
            {"type": "greaterThanOrEquals", "key": "YEAR", "value": "2012"},
            {"type": "lessThanOrEquals", "key": "YEAR", "value": "2024"},
            {"type": "equals", "key": "HAS_COORDINATE", "value": "true"},
            {"type": "equals", "key": "HAS_GEOSPATIAL_ISSUE", "value": "false"},
            {
                "type": "or",
                "predicates": [
                    {"type": "within", "geometry": WKT_BLR},
                    {"type": "within", "geometry": WKT_MYS},
                    {"type": "within", "geometry": WKT_NB}
                ]
            }
        ]
    }

def submit_download():
    if not check_credentials():
        print("ERROR: Incomplete credentials. Cannot submit download.")
        return None
        
    creds = load_credentials()
    username = creds["GBIF_USER"]
    password = creds["GBIF_PWD"]
    email = creds["GBIF_EMAIL"]
    
    payload = {
        "creator": username,
        "notificationAddresses": [email],
        "sendNotification": True,
        "format": "DWCA",
        "predicate": build_predicate()
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request("https://api.gbif.org/v1/occurrence/download/request", data=data)
    req.add_header("Content-Type", "application/json")
    
    # HTTP Basic Authentication
    auth_str = f"{username}:{password}"
    b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("ascii")
    req.add_header("Authorization", f"Basic {b64_auth}")
    
    try:
        with urllib.request.urlopen(req) as resp:
            download_key = resp.read().decode("utf-8").strip()
            print(f"SUCCESS: GBIF Download request submitted successfully!")
            print(f"Download Identifier: {download_key}")
            
            # Save to manifest
            manifest = {
                "download_key": download_key,
                "submission_time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "status": "SUBMITTED",
                "format": "DWCA",
                "expected_records": 3901020,
                "expected_regional_breakdown": {
                    "bengaluru": 2947292,
                    "mysuru": 761890,
                    "nilgiri_bandipur": 191838
                },
                "predicate": payload["predicate"]
            }
            os.makedirs(METADATA_DIR, exist_ok=True)
            with open(MANIFEST_PATH, "w") as f:
                json.dump(manifest, f, indent=2)
            print(f"Saved submission record to {MANIFEST_PATH}")
            return download_key
    except urllib.error.HTTPError as e:
        print(f"HTTP ERROR {e.code}: {e.reason}")
        err_body = e.read().decode("utf-8")
        print(f"Details: {err_body}")
        return None
    except Exception as e:
        print(f"Error submitting download: {e}")
        return None

def check_status(download_key):
    url = f"https://api.gbif.org/v1/occurrence/download/{download_key}"
    req = urllib.request.Request(url, headers={"User-Agent": "DEI_PBL/1.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            meta = json.loads(resp.read().decode("utf-8"))
            status = meta.get("status")
            total_records = meta.get("totalRecords")
            size = meta.get("size")
            doi = meta.get("doi")
            download_link = meta.get("downloadLink")
            
            print(f"Download Key: {download_key}")
            print(f"  Status: {status}")
            print(f"  Total Records: {total_records:,}" if total_records is not None else "  Total Records: Pending")
            print(f"  Size: {size:,} bytes ({size / 1e6:.1f} MB)" if size is not None else "  Size: Pending")
            print(f"  DOI: {doi}")
            print(f"  Download Link: {download_link}")
            return meta
    except Exception as e:
        print(f"Error querying status: {e}")
        return None

def download_archive(download_key):
    meta = check_status(download_key)
    if not meta or meta.get("status") != "SUCCEEDED":
        print(f"Archive is not ready for download. Status: {meta.get('status') if meta else 'UNKNOWN'}")
        return False
        
    download_url = meta.get("downloadLink")
    os.makedirs(RAW_GBIF_DIR, exist_ok=True)
    target_zip = os.path.join(RAW_GBIF_DIR, f"gbif_dei_2012_2024_three_landscapes_dwca.zip")
    part_file = target_zip + ".part"
    
    print(f"\nDownloading archive from: {download_url}")
    print(f"Destination: {target_zip}")
    
    req = urllib.request.Request(download_url, headers={"User-Agent": "DEI_PBL/1.0"})
    with urllib.request.urlopen(req) as resp, open(part_file, "wb") as out_f:
        total_size = int(resp.info().get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 1024 * 4  # 4 MB
        last_log = time.time()
        
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            out_f.write(chunk)
            downloaded += len(chunk)
            if time.time() - last_log > 5:
                pct = (downloaded / total_size * 100) if total_size else 0
                print(f"  Downloaded: {downloaded / 1e6:.1f} MB / {total_size / 1e6:.1f} MB ({pct:.1f}%)")
                last_log = time.time()
                
    # Atomic rename
    os.rename(part_file, target_zip)
    print(f"SUCCESS: Download finished: {target_zip}")
    
    # Calculate SHA-256
    sha256 = hashlib.sha256()
    with open(target_zip, "rb") as f:
        while chunk := f.read(1024 * 1024 * 8):
            sha256.update(chunk)
    hash_hex = sha256.hexdigest()
    print(f"SHA-256 Checksum: {hash_hex}")
    
    # Update manifest
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r") as f:
            manifest = json.load(f)
    else:
        manifest = {}
        
    manifest.update({
        "download_key": download_key,
        "status": "DOWNLOADED",
        "archive_filename": os.path.basename(target_zip),
        "archive_size_bytes": os.path.getsize(target_zip),
        "sha256": hash_hex,
        "doi": meta.get("doi"),
        "total_records": meta.get("totalRecords")
    })
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GBIF DWCA Download Manager")
    parser.add_argument("--check-credentials", action="store_true", help="Check credentials presence")
    parser.add_argument("--submit", action="store_true", help="Submit registered download")
    parser.add_argument("--status", type=str, help="Check status of a download key")
    parser.add_argument("--download", type=str, help="Download completed archive by key")
    
    args = parser.parse_args()
    if args.check_credentials:
        check_credentials()
    elif args.submit:
        submit_download()
    elif args.status:
        check_status(args.status)
    elif args.download:
        download_archive(args.download)
    else:
        parser.print_help()

