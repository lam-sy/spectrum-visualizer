"""Data loading and normalization for allocation, footnote, and spectrum data."""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

import pandas as pd

from .frequency import format_band_label, get_itu_band, parse_frequency_band, ranges_overlap

# Default data directory
DATA_DIR = Path(__file__).parent.parent / "files"


def load_json(filepath: Path) -> Any:
    """Load JSON file and return parsed data."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_allocations(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Load and normalize allocation data from footnotes_by_service.json.
    
    Returns DataFrame with columns:
    - band_start_hz: float
    - band_end_hz: float
    - band_label: str (human-readable like '8.3 kHz - 9 kHz')
    - service: str
    - status: str ('primary' or 'secondary')
    - footnote_ids: list of str
    - itu_band: str (derived from Hz range)
    """
    if filepath is None:
        filepath = DATA_DIR / "footnotes_by_service.json"
    
    data = load_json(filepath)
    
    rows = []
    for item in data:
        band_start = item["band"]["start"]
        band_end = item["band"]["end"]
        
        # Convert footnotes to strings (some are floats like 5.54)
        footnote_ids = [str(fn) for fn in item.get("footnotes", [])]
        
        rows.append({
            "band_start_hz": band_start,
            "band_end_hz": band_end,
            "band_label": format_band_label(band_start, band_end),
            "service": item.get("service", ""),
            "status": item.get("status", ""),
            "footnote_ids": footnote_ids,
            "itu_band": get_itu_band(band_start, band_end),
        })
    
    df = pd.DataFrame(rows)
    
    # Sort by band start frequency
    df = df.sort_values("band_start_hz").reset_index(drop=True)
    
    return df


def load_footnotes(filepath: Optional[Path] = None) -> Dict[str, str]:
    """Load footnote data from footnote.json.
    
    Returns dict mapping Allocation ID -> details text.
    """
    if filepath is None:
        filepath = DATA_DIR / "footnote.json"
    
    data = load_json(filepath)
    
    # Build lookup dict, converting IDs to strings
    footnotes = {}
    for item in data:
        alloc_id = str(item.get("Allocation ID", ""))
        details = item.get("details", "")
        if alloc_id:
            footnotes[alloc_id] = details
    
    return footnotes


def load_applications(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Load and normalize spectrum applications from spectrum.json.
    
    Returns DataFrame with columns:
    - applications: str
    - frequency_bands: str (original string)
    - band_start_hz: float
    - band_end_hz: float
    - max_power: str
    - remarks: str
    """
    if filepath is None:
        filepath = DATA_DIR / "spectrum.json"
    
    data = load_json(filepath)
    
    rows = []
    for item in data:
        freq_band_str = item.get("Frequency bands", "")
        parsed = parse_frequency_band(freq_band_str)
        
        start_hz = parsed[0] if parsed else 0
        end_hz = parsed[1] if parsed else 0
        
        rows.append({
            "applications": item.get("Applications", ""),
            "frequency_bands": freq_band_str,
            "band_start_hz": start_hz,
            "band_end_hz": end_hz,
            "max_power": item.get("Maximum transmit power/ field strength/Conditions", "") or "",
            "remarks": item.get("Reference/Remarks", "") or "",
        })
    
    df = pd.DataFrame(rows)
    
    # Sort by band start frequency
    df = df.sort_values("band_start_hz").reset_index(drop=True)
    
    return df


def get_footnotes_for_ids(footnote_ids: List[str], footnotes_dict: Dict[str, str]) -> pd.DataFrame:
    """Get footnote details for a list of footnote IDs.
    
    Returns DataFrame with columns:
    - footnote_number: str
    - footnote_text: str
    """
    rows = []
    for fn_id in footnote_ids:
        text = footnotes_dict.get(fn_id, "")
        rows.append({
            "footnote_number": fn_id,
            "footnote_text": text,
        })
    
    return pd.DataFrame(rows)


def get_overlapping_applications(
    band_start_hz: float,
    band_end_hz: float,
    applications_df: pd.DataFrame
) -> pd.DataFrame:
    """Get applications whose frequency bands overlap with the given range."""
    if applications_df.empty:
        return applications_df
    
    mask = applications_df.apply(
        lambda row: ranges_overlap(
            band_start_hz, band_end_hz,
            row["band_start_hz"], row["band_end_hz"]
        ),
        axis=1
    )
    
    result = applications_df[mask]
    return pd.DataFrame(result)


def get_unique_services(allocations_df: pd.DataFrame) -> List[str]:
    """Get sorted list of unique service names from allocations."""
    services = allocations_df["service"].unique().tolist()
    return sorted(services)


def get_unique_itu_bands(allocations_df: pd.DataFrame) -> List[str]:
    """Get sorted list of unique ITU bands from allocations."""
    bands = allocations_df["itu_band"].dropna().unique().tolist()
    return sorted(bands)


# Cached data for global access
_allocations_df: Optional[pd.DataFrame] = None
_footnotes_dict: Optional[Dict[str, str]] = None
_applications_df: Optional[pd.DataFrame] = None


def get_allocations() -> pd.DataFrame:
    """Get cached allocations DataFrame."""
    global _allocations_df
    if _allocations_df is None:
        _allocations_df = load_allocations()
    return _allocations_df


def get_footnotes() -> Dict[str, str]:
    """Get cached footnotes dictionary."""
    global _footnotes_dict
    if _footnotes_dict is None:
        _footnotes_dict = load_footnotes()
    return _footnotes_dict


def get_applications() -> pd.DataFrame:
    """Get cached applications DataFrame."""
    global _applications_df
    if _applications_df is None:
        _applications_df = load_applications()
    return _applications_df


def reload_all_data():
    """Reload all cached data from files."""
    global _allocations_df, _footnotes_dict, _applications_df
    _allocations_df = load_allocations()
    _footnotes_dict = load_footnotes()
    _applications_df = load_applications()
