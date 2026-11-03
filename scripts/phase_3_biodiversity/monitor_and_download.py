#!/usr/bin/env python3
"""
Dark Ecology Intelligence (DEI) — Phase 3
Script: monitor_and_download.py

Monitors registered GBIF download 0025038-261023074918325 until SUCCEEDED,
downloads the DWCA zip archive using atomic .part renaming,
computes SHA-256, and extracts the core files.
"""

import os
import sys
import json
import time
import hashlib
import zipfile
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
RAW_GBIF_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "gbif")
METADATA_DIR = os.path.join(PROJECT_ROOT, "data", "metadata")
MANIFEST_PATH = os.path.join(METADATA_DIR, "gbif_download_manifest.json")

DOWNLOAD_KEY = "0025038-261023074918325"
ZIP_NAME = "gbif_dei_2012_2024_three_landscapes_dwca.zip"
TARGET_ZIP = os.path.join(RAW_GBIF_DIR, ZIP_NAME)
PART_FILE = TARGET_ZIP + ".part"
EXTRACTED_DIR = os.path.join(RAW_GBIF_DIR, "extracted")

def monitor_and_retrieve():
    url = f"https://api.gbif.org/v1/occurrence/download/{DOWNLOAD_KEY}"
    print(f"Starting monitor for GBIF Download: {DOWNLOAD_KEY}")
    print(f"Polling endpoint: {url}")
    
    start_time = time.time()
    last_status = None
    
    while True:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "DEI_PBL/1.0"})
            with urllib.request.urlopen(req) as resp:
                meta = json.loads(resp.read().decode("utf-8"))
                status = meta.get("status")
                
                if status != last_status:
                    elapsed = int(time.time() - start_time)
                    print(f"[{elapsed}s] GBIF Download Status: {status}")
                    last_status = status
                    
                if status == "SUCCEEDED":
                    print("\n=== GBIF DOWNLOAD SUCCEEDED ===")
                    print(f"DOI: {meta.get('doi')}")
                    print(f"Total Records: {meta.get('totalRecords'):,}")
                    print(f"Archive Size: {meta.get('size'):,} bytes ({meta.get('size') / 1e6:.1f} MB)")
                    print(f"Download URL: {meta.get('downloadLink')}")
                    return meta
                elif status in ["FAILED", "KILLED", "CANCELLED"]:
                    print(f"\nFATAL: Download terminated with status: {status}")
                    sys.exit(1)
        except Exception as e:
            print(f"Transient error polling status: {e}")
            
        time.sleep(20)

def download_file(meta):
    download_url = meta.get("downloadLink")
    os.makedirs(RAW_GBIF_DIR, exist_ok=True)
    
    print(f"\n--- Initiating Archive Download ---")
    print(f"Source: {download_url}")
    print(f"Destination (temp): {PART_FILE}")
    print(f"Final target: {TARGET_ZIP}")
    
    req = urllib.request.Request(download_url, headers={"User-Agent": "DEI_PBL/1.0"})
    with urllib.request.urlopen(req) as resp, open(PART_FILE, "wb") as out_f:
        total_size = int(resp.info().get("Content-Length", meta.get("size", 0)))
        downloaded = 0
        chunk_size = 1024 * 1024 * 4  # 4 MB
        last_log = time.time()
        start_dl = time.time()
        
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            out_f.write(chunk)
            downloaded += len(chunk)
            if time.time() - last_log >= 5:
                pct = (downloaded / total_size * 100) if total_size else 0
                mb = downloaded / 1e6
                tot_mb = total_size / 1e6
                speed = mb / max(time.time() - start_dl, 0.1)
                print(f"  Progress: {mb:.1f} MB / {tot_mb:.1f} MB ({pct:.1f}%) @ {speed:.1f} MB/s")
                last_log = time.time()
                
    # Atomic rename
    os.rename(PART_FILE, TARGET_ZIP)
    file_size = os.path.getsize(TARGET_ZIP)
    print(f"\nSUCCESS: Download completed! Saved to {TARGET_ZIP} ({file_size:,} bytes)")
    
    # Checksum calculation
    print("Calculating SHA-256 checksum...")
    sha256 = hashlib.sha256()
    with open(TARGET_ZIP, "rb") as f:
        while chunk := f.read(1024 * 1024 * 8):
            sha256.update(chunk)
    hash_hex = sha256.hexdigest()
    print(f"SHA-256: {hash_hex}")
    
    # Update manifest
    manifest = {
        "download_key": DOWNLOAD_KEY,
        "status": "DOWNLOADED",
        "archive_filename": ZIP_NAME,
        "archive_size_bytes": file_size,
        "sha256": hash_hex,
        "doi": meta.get("doi"),
        "total_records": meta.get("totalRecords"),
        "created_utc": meta.get("created"),
        "download_link": meta.get("downloadLink"),
        "format": "DWCA",
        "expected_records": 3901020,
        "expected_regional_breakdown": {
            "bengaluru": 2947292,
            "mysuru": 761890,
            "nilgiri_bandipur": 191838
        }
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Updated manifest at {MANIFEST_PATH}")
    return hash_hex

def extract_archive():
    print(f"\n--- Extracting Archive into {EXTRACTED_DIR} ---")
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    with zipfile.ZipFile(TARGET_ZIP, 'r') as zf:
        file_list = zf.namelist()
        print(f"Archive contains {len(file_list)} files: {file_list}")
        for item in file_list:
            zf.extract(item, EXTRACTED_DIR)
            sz = os.path.getsize(os.path.join(EXTRACTED_DIR, item))
            print(f"  Extracted: {item} ({sz:,} bytes / {sz/1e6:.1f} MB)")
            
    print("SUCCESS: Extraction complete!")

if __name__ == "__main__":
    meta = monitor_and_retrieve()
    sha256 = download_file(meta)
    extract_archive()

