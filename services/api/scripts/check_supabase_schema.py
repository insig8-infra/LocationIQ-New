from typing import List

from postgrest import APIError

from app.core.config import get_settings
from app.repositories.supabase_repo import SupabaseReportRepository


REQUIRED_TABLES: List[str] = [
    "report_requests",
    "report_locations",
    "reverse_geocode_results",
    "s2_cells",
    "s2_cell_features",
    "location_cell_profiles",
    "previews",
    "payments",
    "source_runs",
    "raw_artifacts",
    "normalized_observations",
    "pois",
    "catchments",
    "travel_times",
    "public_web_sessions",
    "pricing_records",
    "signals",
    "visual_assets",
    "reports",
    "audit_events",
]

REQUIRED_COLUMNS = {
    "report_requests": [
        "id",
        "public_token",
        "email",
        "location_input",
        "use_case_input",
        "status",
        "payment_status",
        "current_stage",
        "progress_percent",
    ],
    "report_locations": [
        "id",
        "report_request_id",
        "selected_latitude",
        "selected_longitude",
        "geom",
        "address_text",
        "locality",
        "city",
        "state",
        "pin_code",
        "s2_l12_cell_id",
        "s2_l13_cell_id",
        "s2_l14_cell_id",
        "s2_l15_cell_id",
        "s2_l16_cell_id",
    ],
    "reverse_geocode_results": [
        "id",
        "location_id",
        "provider",
        "provider_place_id",
        "response_json",
    ],
    "previews": ["id", "report_request_id", "preview_json", "cost_class"],
    "payments": [
        "id",
        "report_request_id",
        "provider",
        "checkout_session_id",
        "payment_id",
        "status",
    ],
    "reports": [
        "id",
        "report_request_id",
        "public_token",
        "schema_version",
        "report_json",
        "status",
    ],
}


def main() -> int:
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        print("Supabase URL or service role key is missing.")
        return 2

    repo = SupabaseReportRepository(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
    )
    missing = []
    for table in REQUIRED_TABLES:
        select_clause = ",".join(REQUIRED_COLUMNS.get(table, ["*"]))
        try:
            repo.client.table(table).select(select_clause).limit(1).execute()
        except APIError as exc:
            missing.append((table, exc.message))

    if missing:
        print("Supabase schema is not ready:")
        for table, message in missing:
            print(f"- {table}: {message}")
        return 1

    print("Supabase schema check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
