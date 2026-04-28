from app.models import Pin, PreviewContent, PurposeSummary


LOCKED_SECTIONS = [
    "Exact pin and plot read",
    "Catchment and access",
    "Nearby competitors and anchors",
    "Public platform signals",
    "Pricing and spend cues",
    "Visual evidence pack",
    "What to verify physically",
]


def generate_preview(pin: Pin, purpose: PurposeSummary, preview_safe_summary: str) -> PreviewContent:
    location_label = pin.locality or pin.city or f"{pin.latitude:.6f}, {pin.longitude:.6f}"
    return PreviewContent(
        headline=f"Location preview for {purpose.display_label} near {location_label}",
        pin_summary=(
            f"The report will analyse the exact coordinate {pin.latitude:.6f}, "
            f"{pin.longitude:.6f}, not the nearest named POI."
        ),
        location_character_teaser=preview_safe_summary,
        preview_points=[
            "The full report will separate exact-pin context from broader locality signals.",
            "It will build purpose-specific catchments before interpreting demand or access.",
            "Public platform and POI signals will be collected only where they are location-conditioned.",
            "Visible prices will only be compared when slot duration and unit can be normalized.",
        ],
        locked_sections=LOCKED_SECTIONS,
    )

