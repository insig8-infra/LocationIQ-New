import math
import re
from typing import Any, Dict, List, Optional, Tuple

import httpx
from fastapi import HTTPException, status

from app.core.config import get_settings
from app.models import Pin


COORDINATE_RE = re.compile(
    r"(?P<lat>[+-]?(?:[1-8]?\d(?:\.\d+)?|90(?:\.0+)?))\s*,\s*"
    r"(?P<lng>[+-]?(?:(?:1[0-7]\d|[1-9]?\d)(?:\.\d+)?|180(?:\.0+)?))"
)
GOOGLE_AT_RE = re.compile(r"@(?P<lat>-?\d+(?:\.\d+)?),(?P<lng>-?\d+(?:\.\d+)?)")
GOOGLE_BANG_RE = re.compile(r"!3d(?P<lat>-?\d+(?:\.\d+)?)!4d(?P<lng>-?\d+(?:\.\d+)?)")
GOOGLE_QUERY_RE = re.compile(r"[?&]query=(?P<query>-?\d+(?:\.\d+)?%2C-?\d+(?:\.\d+)?)")
HTTP_URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def resolve_location(location_input: str) -> Tuple[Pin, Dict[str, Any]]:
    settings = get_settings()
    expanded_input = expand_short_link(location_input)
    coordinate = parse_coordinates(expanded_input) or parse_coordinates(location_input)
    provider_results: List[Dict[str, Any]] = []

    if coordinate is None and settings.google_maps_api_key:
        coordinate, forward_result = google_forward_geocode(
            location_input,
            settings.google_maps_api_key,
        )
        if forward_result:
            provider_results.append(forward_result)

    if coordinate is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "ambiguous_location",
                "message": (
                    "Could not extract or geocode a coordinate. Please paste a dropped-pin "
                    "Google Maps URL or latitude,longitude pair."
                ),
            },
        )

    latitude, longitude = coordinate
    if settings.google_maps_api_key:
        google_result = google_reverse_geocode(latitude, longitude, settings.google_maps_api_key)
        if google_result:
            provider_results.append(google_result)
    if settings.mappls_rest_api_key:
        mappls_result = mappls_reverse_geocode(latitude, longitude, settings.mappls_rest_api_key)
        if mappls_result:
            provider_results.append(mappls_result)

    pin = build_pin(latitude, longitude, provider_results)
    profile = build_cell_profile(latitude, longitude)
    profile["reverse_geocode_results"] = provider_results
    profile["expanded_location_input"] = expanded_input
    profile["provider_count"] = len(provider_results)
    return pin, profile


def parse_coordinates(location_input: str) -> Optional[Tuple[float, float]]:
    decoded = location_input.replace("%2C", ",").replace("%2c", ",")
    for pattern in (GOOGLE_AT_RE, GOOGLE_BANG_RE, COORDINATE_RE):
        match = pattern.search(decoded)
        if match:
            return float(match.group("lat")), float(match.group("lng"))

    query_match = GOOGLE_QUERY_RE.search(location_input)
    if query_match:
        query = query_match.group("query").replace("%2C", ",")
        return parse_coordinates(query)
    return None


def expand_short_link(location_input: str) -> str:
    if not HTTP_URL_RE.match(location_input):
        return location_input
    try:
        with httpx.Client(follow_redirects=True, timeout=8.0) as client:
            response = client.get(location_input)
            return str(response.url)
    except httpx.HTTPError:
        return location_input


def google_forward_geocode(address: str, api_key: str) -> Tuple[Optional[Tuple[float, float]], Optional[Dict[str, Any]]]:
    try:
        response = httpx.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": address, "region": "in", "key": api_key},
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError):
        return None, provider_error("google_geocoding", "forward_geocode_failed")

    if payload.get("status") != "OK" or not payload.get("results"):
        return None, provider_error(
            "google_geocoding",
            f"forward_geocode_status_{payload.get('status', 'unknown').lower()}",
            payload,
        )

    result = payload["results"][0]
    location = result["geometry"]["location"]
    provider_result = normalize_google_result(result, "forward_geocode", (location["lat"], location["lng"]))
    return (float(location["lat"]), float(location["lng"])), provider_result


def google_reverse_geocode(latitude: float, longitude: float, api_key: str) -> Optional[Dict[str, Any]]:
    try:
        response = httpx.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"latlng": f"{latitude},{longitude}", "key": api_key},
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError):
        return provider_error("google_geocoding", "reverse_geocode_failed")

    if payload.get("status") != "OK" or not payload.get("results"):
        return provider_error(
            "google_geocoding",
            f"reverse_geocode_status_{payload.get('status', 'unknown').lower()}",
            payload,
        )

    return normalize_google_result(payload["results"][0], "reverse_geocode", (latitude, longitude))


def normalize_google_result(
    result: Dict[str, Any],
    collection_type: str,
    selected_coordinate: Tuple[float, float],
) -> Dict[str, Any]:
    components = result.get("address_components", [])
    location = result.get("geometry", {}).get("location", {})
    resolved_lat = location.get("lat")
    resolved_lng = location.get("lng")
    return {
        "provider": "google_geocoding",
        "collection_type": collection_type,
        "provider_place_id": result.get("place_id"),
        "address_text": result.get("formatted_address"),
        "locality": component_value(
            components,
            ["sublocality_level_1", "sublocality", "neighborhood", "locality"],
        ),
        "city": component_value(
            components,
            ["locality", "administrative_area_level_3", "administrative_area_level_2"],
        ),
        "district": component_value(components, ["administrative_area_level_3"]),
        "state": component_value(components, ["administrative_area_level_1"]),
        "pin_code": component_value(components, ["postal_code"]),
        "plus_code": result.get("plus_code", {}).get("global_code"),
        "resolved_latitude": resolved_lat,
        "resolved_longitude": resolved_lng,
        "distance_from_selected_m": distance_m(
            selected_coordinate[0],
            selected_coordinate[1],
            resolved_lat,
            resolved_lng,
        ),
        "response_json": result,
        "cache_policy": "provider_terms_required",
        "user_facing_source_note": "Google reverse geocoding was used for address context only.",
    }


def mappls_reverse_geocode(latitude: float, longitude: float, access_token: str) -> Optional[Dict[str, Any]]:
    try:
        response = httpx.get(
            "https://search.mappls.com/search/address/rev-geocode",
            params={"lat": latitude, "lng": longitude, "access_token": access_token},
            timeout=10.0,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError):
        return provider_error("mappls_reverse_geocoding", "reverse_geocode_failed")

    results = payload.get("results") or []
    if not results:
        return provider_error("mappls_reverse_geocoding", "reverse_geocode_empty", payload)

    first = results[0]
    resolved_lat = first.get("latitude") or first.get("lat")
    resolved_lng = first.get("longitude") or first.get("lng")
    return {
        "provider": "mappls_reverse_geocoding",
        "collection_type": "reverse_geocode",
        "provider_place_id": first.get("eLoc") or first.get("place_id"),
        "address_text": first.get("address") or first.get("formatted_address"),
        "locality": first.get("locality") or first.get("subLocality") or first.get("poi"),
        "city": first.get("city"),
        "district": first.get("district"),
        "state": first.get("state"),
        "pin_code": first.get("pincode") or first.get("pin_code"),
        "resolved_latitude": resolved_lat,
        "resolved_longitude": resolved_lng,
        "distance_from_selected_m": distance_m(latitude, longitude, resolved_lat, resolved_lng),
        "response_json": first,
        "cache_policy": "provider_terms_required",
        "user_facing_source_note": "Mappls reverse geocoding was used for India address context only.",
    }


def build_pin(latitude: float, longitude: float, provider_results: List[Dict[str, Any]]) -> Pin:
    usable_results = [result for result in provider_results if "address_text" in result]
    best = usable_results[0] if usable_results else {}
    disagreement = provider_disagreement_note(usable_results)
    if not usable_results:
        note = (
            "The coordinate is precise. Reverse geocoding did not return usable address "
            "context in this pass, so nearby named places are not used as identity."
        )
    elif disagreement:
        note = (
            "The coordinate is precise. Address providers disagree on some locality context; "
            "the marker remains the report identity."
        )
    else:
        note = (
            "The coordinate is precise. Address and nearby place names are context only; "
            "the marker remains the report identity."
        )

    return Pin(
        latitude=latitude,
        longitude=longitude,
        address_text=best.get("address_text") or "Address context unavailable",
        locality=best.get("locality"),
        city=best.get("city"),
        district=best.get("district"),
        state=best.get("state"),
        pin_code=best.get("pin_code"),
        plus_code=best.get("plus_code"),
        geocode_quality_note=note,
    )


def provider_disagreement_note(provider_results: List[Dict[str, Any]]) -> bool:
    if len(provider_results) < 2:
        return False
    localities = {normalize_text(result.get("locality")) for result in provider_results if result.get("locality")}
    cities = {normalize_text(result.get("city")) for result in provider_results if result.get("city")}
    states = {normalize_text(result.get("state")) for result in provider_results if result.get("state")}
    return len(localities) > 1 or len(cities) > 1 or len(states) > 1


def provider_error(provider: str, message: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "provider": provider,
        "collection_type": "provider_error",
        "error": message,
        "response_json": payload or {},
        "cache_policy": "do_not_cache",
        "user_facing_source_note": f"{provider} could not provide address context in this pass.",
    }


def component_value(components: List[Dict[str, Any]], preferred_types: List[str]) -> Optional[str]:
    for preferred_type in preferred_types:
        for component in components:
            if preferred_type in component.get("types", []):
                return component.get("long_name")
    return None


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def distance_m(lat1: float, lng1: float, lat2: Any, lng2: Any) -> Optional[float]:
    if lat2 is None or lng2 is None:
        return None
    try:
        lat2_float = float(lat2)
        lng2_float = float(lng2)
    except (TypeError, ValueError):
        return None

    radius_m = 6_371_000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2_float)
    delta_phi = math.radians(lat2_float - lat1)
    delta_lambda = math.radians(lng2_float - lng1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return round(radius_m * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


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


def s2_levels_available(cell_profile: Dict[str, Any]) -> List[str]:
    return sorted(cell_profile.get("cells", {}).keys())
