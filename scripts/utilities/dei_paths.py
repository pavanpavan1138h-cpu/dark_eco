"""Project path helpers for the DEI project.

Every notebook imports this module so that paths are always *relative to the
project root* (the `dark_eco/` folder) and never hard-coded to one computer.
"""
from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    """Walk upwards from `start` until the folder containing the
    `.dei_project_root` marker file is found."""
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / ".dei_project_root").exists():
            return candidate
    raise FileNotFoundError(
        "Could not find the DEI project root (missing .dei_project_root marker). "
        "Run the notebook from inside the dark_eco/ folder."
    )


ROOT = find_project_root(Path(__file__).parent)

DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
METADATA = DATA / "metadata"
EXTERNAL_REFS = DATA / "external_references"
BOUNDARIES = ROOT / "geographical_boundaries"
REPORTS = ROOT / "reports"
LOGS = ROOT / "logs"

