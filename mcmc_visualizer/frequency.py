"""Frequency utility functions: Hz conversions, parsing, formatting, and ITU band mapping."""

import re
from typing import Tuple, Optional

# Frequency unit multipliers to Hz
UNIT_TO_HZ = {
    "hz": 1,
    "khz": 1e3,
    "mhz": 1e6,
    "ghz": 1e9,
    "thz": 1e12,
}

# ITU band definitions (name -> (start_hz, end_hz))
ITU_BANDS = {
    "VLF (3-30 kHz)": (3e3, 30e3),
    "LF (30-300 kHz)": (30e3, 300e3),
    "MF (300-3000 kHz)": (300e3, 3000e3),
    "HF (3-30 MHz)": (3e6, 30e6),
    "VHF (30-300 MHz)": (30e6, 300e6),
    "UHF (300-1000 MHz)": (300e6, 1000e6),
    "L (1-2 GHz)": (1e9, 2e9),
    "S (2-4 GHz)": (2e9, 4e9),
    "C (4-8 GHz)": (4e9, 8e9),
    "X (8-12 GHz)": (8e9, 12e9),
    "Ku (12-18 GHz)": (12e9, 18e9),
    "K (18-27 GHz)": (18e9, 27e9),
    "Ka (27-40 GHz)": (27e9, 40e9),
    "V (40-75 GHz)": (40e9, 75e9),
    "W (75-110 GHz)": (75e9, 110e9),
    "mm or G (110-300 GHz)": (110e9, 300e9),
}

# Ordered list of ITU band names for dropdown
ITU_BAND_OPTIONS = ["All"] + list(ITU_BANDS.keys())


def hz_to_unit(hz: float) -> Tuple[float, str]:
    """Convert Hz to the most appropriate human-readable unit.
    
    Returns:
        Tuple of (value, unit_string)
    """
    if hz >= 1e12:
        return hz / 1e12, "THz"
    elif hz >= 1e9:
        return hz / 1e9, "GHz"
    elif hz >= 1e6:
        return hz / 1e6, "MHz"
    elif hz >= 1e3:
        return hz / 1e3, "kHz"
    else:
        return hz, "Hz"


def format_frequency(hz: float) -> str:
    """Format Hz value to human-readable string like '8.3 kHz'."""
    value, unit = hz_to_unit(hz)
    # Remove trailing zeros after decimal
    if value == int(value):
        return f"{int(value)} {unit}"
    else:
        return f"{value:g} {unit}"


def format_band_label(start_hz: float, end_hz: float) -> str:
    """Format a frequency band range like '8.3 kHz - 9 kHz'."""
    return f"{format_frequency(start_hz)} - {format_frequency(end_hz)}"


def parse_frequency(freq_str: str) -> Optional[float]:
    """Parse a frequency string like '8.3 kHz' or '2.4 GHz' to Hz.
    
    Returns:
        Frequency in Hz, or None if parsing fails.
    """
    if not freq_str:
        return None
    
    freq_str = freq_str.strip().lower()
    
    # Match patterns like "8.3 khz", "2.4ghz", "100 mhz"
    pattern = r"^([\d.]+)\s*(hz|khz|mhz|ghz|thz)?$"
    match = re.match(pattern, freq_str)
    
    if match:
        value = float(match.group(1))
        unit = match.group(2) or "hz"
        return value * UNIT_TO_HZ.get(unit, 1)
    
    return None


def parse_frequency_band(band_str: str) -> Optional[Tuple[float, float]]:
    """Parse a frequency band string like '3155 kHz to 3400 kHz' to (start_hz, end_hz).
    
    Handles various formats:
    - '3155 kHz to 3400 kHz'
    - '26.957 MHz to 27.283 MHz'
    - '5.48 MHz - 5.68 MHz'
    
    Returns:
        Tuple of (start_hz, end_hz), or None if parsing fails.
    """
    if not band_str:
        return None
    
    band_str = band_str.strip()
    
    # Pattern for "X unit to/- Y unit"
    pattern = r"^([\d.]+)\s*(Hz|kHz|MHz|GHz|THz)?\s*(?:to|-)\s*([\d.]+)\s*(Hz|kHz|MHz|GHz|THz)?$"
    match = re.match(pattern, band_str, re.IGNORECASE)
    
    if match:
        start_val = float(match.group(1))
        start_unit = (match.group(2) or "Hz").lower()
        end_val = float(match.group(3))
        end_unit = (match.group(4) or match.group(2) or "Hz").lower()  # Fallback to start unit
        
        start_hz = start_val * UNIT_TO_HZ.get(start_unit, 1)
        end_hz = end_val * UNIT_TO_HZ.get(end_unit, 1)
        
        return start_hz, end_hz
    
    return None


def value_with_unit_to_hz(value: float, unit: str) -> float:
    """Convert a numeric value with unit string to Hz."""
    unit_lower = unit.lower().replace(" ", "")
    return value * UNIT_TO_HZ.get(unit_lower, 1)


def get_itu_band(start_hz: float, end_hz: float) -> Optional[str]:
    """Determine which ITU band(s) a frequency range falls into.
    
    Returns the first matching band, or None if no match.
    """
    mid_hz = (start_hz + end_hz) / 2
    
    for band_name, (band_start, band_end) in ITU_BANDS.items():
        if band_start <= mid_hz <= band_end:
            return band_name
    
    return None


def ranges_overlap(start1: float, end1: float, start2: float, end2: float) -> bool:
    """Check if two frequency ranges overlap."""
    return start1 < end2 and start2 < end1
