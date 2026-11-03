"""Polite HTTP helpers used by DEI notebooks.

* Sends an identifying User-Agent (required by OpenStreetMap Nominatim policy).
* Retries transient failures with back-off.
* Never stores credentials. Any service needing a key reads it from an
  environment variable and fails loudly if the variable is absent.
"""
from __future__ import annotations

import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

USER_AGENT = "DEI-ANN-PBL/0.1 (academic student research project; non-commercial)"
HEADERS = {"User-Agent": USER_AGENT}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url: str, params: dict | None = None, timeout: int = 60,
        retries: int = 3, pause: float = 1.0, **kwargs) -> requests.Response:
    """GET with retries. Sleeps `pause` seconds after each call (rate-limit courtesy)."""
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=timeout, **kwargs)
            time.sleep(pause)
            if resp.status_code in (429, 502, 503, 504) and attempt < retries:
                time.sleep(pause * 2 ** attempt)
                continue
            return resp
        except requests.RequestException as exc:  # network problem
            last_exc = exc
            time.sleep(pause * 2 ** attempt)
    raise RuntimeError(f"GET failed after {retries} attempts: {url} ({last_exc})")


def check_url(url: str, timeout: int = 30) -> dict:
    """Check whether a documentation/portal URL resolves. Returns status info.

    Uses a streamed GET (many portals reject HEAD) and closes the connection
    without downloading the body.
    """
    info = {"url": url, "checked_utc": utc_now()}
    try:
        with requests.get(url, headers=HEADERS, timeout=timeout, stream=True,
                          allow_redirects=True) as r:
            info.update(http_status=r.status_code, final_url=r.url, error="")
    except requests.RequestException as exc:
        info.update(http_status=None, final_url="", error=type(exc).__name__)
    return info


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

