"""Configuration constants for the Priva PDF application."""

from src.pdf_compressor import CompressionLevel

# Compression level options for dropdowns
COMPRESSION_OPTIONS = [
    {"label": "Low", "value": "LOW"},
    {"label": "Medium", "value": "MEDIUM"},
    {"label": "High", "value": "HIGH"},
    {"label": "Extreme", "value": "EXTREME"},
]

# Descriptions for each compression level
COMPRESSION_DESCRIPTIONS = {
    "LOW": "Minimal compression, best quality (85% quality, no scaling)",
    "MEDIUM": "Balanced compression (65% quality, 85% scale)",
    "HIGH": "Strong compression, smaller file (45% quality, 70% scale)",
    "EXTREME": "Maximum compression, lowest quality (25% quality, 50% scale)",
}

# Map string values to CompressionLevel enum
COMPRESSION_LEVEL_MAP = {
    "LOW": CompressionLevel.LOW,
    "MEDIUM": CompressionLevel.MEDIUM,
    "HIGH": CompressionLevel.HIGH,
    "EXTREME": CompressionLevel.EXTREME,
}


def get_compression_level(level_str: str) -> CompressionLevel:
    """Convert string level to CompressionLevel enum."""
    return COMPRESSION_LEVEL_MAP.get(level_str, CompressionLevel.MEDIUM)
