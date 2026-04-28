from typing import Any, Dict

from app.models import Pin, PurposeSummary, utc_now


def generate_demo_report(
    *,
    report_id: str,
    location_input: str,
    pin: Pin,
    purpose: PurposeSummary,
) -> Dict[str, Any]:
    source_ref = "local_mock_source_run"
    generated_at = utc_now().isoformat()
    return {
        "metadata": {
            "report_id": report_id,
            "generated_at": generated_at,
            "report_mode": "reader_first_location_intelligence",
            "location_input": location_input,
            "selected_pin": {
                "latitude": pin.latitude,
                "longitude": pin.longitude,
                "address_text": pin.address_text or "",
                "geocode_quality_note": pin.geocode_quality_note or "",
            },
            "purpose_category": purpose.purpose_category,
            "sub_purpose": purpose.sub_purpose,
            "selected_context": {},
            "data_coverage_note": (
                "This is a local demo report generated before external source connectors are "
                "configured. It preserves the exact pin and shows the intended report shape."
            ),
        },
        "reader_summary": {
            "headline": f"Early location read for {purpose.display_label}",
            "summary": (
                "You are looking at an exact coordinate. This demo report does not yet make "
                "market claims because provider source collection is not connected."
            ),
            "what_looks_useful": [
                {
                    "title": "Exact pin retained",
                    "text": "The selected coordinate is preserved as the report identity.",
                    "source_refs": [source_ref],
                }
            ],
            "what_can_create_friction": [
                {
                    "title": "Provider data pending",
                    "text": "Reverse geocoding, POI, routing, and public-web checks still need live connectors.",
                    "source_refs": [source_ref],
                }
            ],
            "what_to_verify": [
                {
                    "title": "Ground truth",
                    "text": "Visit the exact pin and confirm access, frontage, operating constraints, and local context.",
                    "source_refs": [source_ref],
                }
            ],
        },
        "purpose_lens": {
            "understanding_question": f"What is this exact location like for {purpose.display_label}?",
            "what_matters": [
                "Exact pin context",
                "Catchment and access",
                "Relevant anchors and competitors",
                "Source-backed numbers",
            ],
            "excluded_or_not_claimed": [
                "No buy/open/invest verdict",
                "No legal parcel boundary claim",
                "No unsupported demand certainty",
            ],
        },
        "exact_pin": {
            "pin_read": (
                f"The selected coordinate is {pin.latitude:.6f}, {pin.longitude:.6f}. "
                "Nearby named places must be treated as orientation only."
            ),
            "nearest_poi_policy": "Nearest POIs are context, never identity.",
            "plot_visualization": {
                "visual_type": "exact_marker",
                "caption": "Exact marker only. No legal boundary is claimed.",
                "is_legal_boundary": False,
                "source_refs": [source_ref],
            },
            "not_claimed": ["legal boundary", "physical suitability", "market success"],
        },
        "multi_anchor_story": [
            {
                "layer": "exact_pin",
                "what_is_visible": "The exact coordinate is available and preserved.",
                "how_it_should_shape_the_view": (
                    "All later locality, POI, and public-web claims should be tied back to this coordinate."
                ),
                "source_refs": [source_ref],
            }
        ],
        "catchment_and_reach": [
            {
                "catchment": "exact_pin",
                "character": "Catchment generation is pending routing and map connectors.",
                "purpose_meaning": (
                    "The first production pass will add distance rings and travel-time views before "
                    "making access claims."
                ),
                "key_numbers": [],
                "source_refs": [source_ref],
            }
        ],
        "arrival_reality": {
            "summary": "Routing providers are not connected yet.",
            "interpretation": [
                "Arrival, final turn, and parking/drop-off context should be checked after route collection."
            ],
            "source_refs": [source_ref],
        },
        "key_numbers": [],
        "competition_and_pricing": {
            "summary": "Competitor and pricing collection is pending live connectors.",
            "competitors": [],
            "pricing_records": [],
            "pricing_normalization_note": (
                "No prices are compared until slot duration and unit are captured."
            ),
        },
        "spend_and_convenience": {
            "summary": "Public platform and quick-commerce checks are not connected yet.",
            "interpretation": [
                "Spend and convenience claims are intentionally withheld until location-conditioned sources are collected."
            ],
            "source_refs": [source_ref],
        },
        "locality_conditions": [],
        "visual_evidence_pack": [
            {
                "visual_type": "exact_pin_map",
                "title": "Exact pin map",
                "purpose": "Show the coordinate the report is analysing.",
                "caption": "Map rendering will use the configured Maps provider in the web UI.",
                "source_refs": [source_ref],
            }
        ],
        "field_verification_plan": [
            {
                "visit_window": "Relevant operating daypart for the selected use case",
                "what_to_check": [
                    "Confirm the usable entrance or frontage for the exact pin.",
                    "Observe approach, drop-off, parking, and immediate physical friction.",
                    "Compare what is visible on the ground against the generated report notes.",
                ],
                "why_it_matters": "The selected coordinate can still differ from a usable entrance or plot access.",
            }
        ],
        "source_notes": [
            {
                "id": source_ref,
                "name": "Local mock source",
                "source_type": "open_map",
                "last_checked": generated_at,
                "spatial_resolution": "exact coordinate supplied by user input",
                "pin_conditioned": True,
                "used_for": ["local development report shape"],
                "user_facing_note": (
                    "Used only for local development before provider integrations are enabled."
                ),
                "limitations": ["No live provider source collection has been run."],
            }
        ],
    }
