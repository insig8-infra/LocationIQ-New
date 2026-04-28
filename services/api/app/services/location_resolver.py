import re
from typing import Any, Dict, List, Tuple

from fastapi import HTTPException, status

from app.models import Pin


COORDINATE_RE = re.compile(
    r"(?P<lat>[+-]?(?:[1-8]?\d(?:\.\d+)?|90(?:\.0+)?))\s*,\s*"
    r"(?P<lng>[+-]?(?:(?:1[0-7]\d|[1-9]?\d)(?:\.\d+)?|180(?:\.0+)?))"
)
GOOGLE_AT_RE = re.compile(r"@(?P<lat>-?\d+(?:\.\d+)?),(?P<lng>-?\d+(?:\.\d+)?)")
GOOGLE_BANG_RE = re.compile(r"!3d(?P<lat>-?\d+(?:\.\d+)?)!4d(?P<lng>-?\d+(?:\.\d+)?)")


def parse_coordinates(location_input: str) -> Tuple[float, float]:
    for pattern in (GOOGLE_AT_RE, GOOGLE_BANG_RE, COORDINATE_RE):
        match = pattern.search(location_input)
        if match:
            return float(match.group("lat")), float(match.group("lng"))

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "code": "ambiguous_location",
            "message": (
                "This build can parse coordinates or map URLs containing coordinates. "
                "Provider geocoding is not connected yet."
            ),
        },
    )


def deterministic_cell_token(latitude: float, longitude: float, level: int) -> str:
    # Placeholder until a real S2 Geometry implementation is wired in.
    scale = 2 ** max(level - 10, 0)
    lat_bucket = int((latitude + 90) * scale)
    lng_bucket = int((longitude + 180) * scale)
    return f"mock_s2_l{level}_{lat_bucket}_{lng_bucket}"


def build_cell_profile(latitude: float, longitude: float) -> Dict[str, Any]:
    cells = {
        f"L{level}": deterministic_cell_token(latitude, longitude, level)
        for level in range(12, 17)
    }
    return {
        "cells": cells,
        "profile_labels": ["profile_pending_provider_data"],
        "profile_status": "generated",
        "preview_safe_summary": (
            "The exact coordinate has been converted into multi-resolution location cells. "
            "The full profile will become more specific once POI, access, and public-web "
            "signals are collected."
        ),
        "data_limit_note": (
            "This local build uses deterministic placeholder cell IDs until an S2 Geometry "
            "library is connected."
        ),
    }


def resolve_location(location_input: str) -> Tuple[Pin, Dict[str, Any]]:
    latitude, longitude = parse_coordinates(location_input)
    profile = build_cell_profile(latitude, longitude)
    pin = Pin(
        latitude=latitude,
        longitude=longitude,
        address_text="Provider geocoding pending",
        locality=None,
        city=None,
        state=None,
        geocode_quality_note=(
            "The coordinate is precise. Reverse geocoding providers are not connected in "
            "this local build, so nearby named places are not used as identity."
        ),
    )
    return pin, profile


def s2_levels_available(cell_profile: Dict[str, Any]) -> List[str]:
    return sorted(cell_profile.get("cells", {}).keys())

