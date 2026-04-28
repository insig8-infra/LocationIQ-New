from typing import List

from postgrest import APIError

from app.core.config import get_settings
from app.repositories.supabase_repo import SupabaseReportRepository


REQUIRED_TABLES: List[str] = [
    "report_requests",
    "locations",
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
        try:
            repo.client.table(table).select("*").limit(1).execute()
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
