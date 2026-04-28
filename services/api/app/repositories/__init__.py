from app.core.config import get_settings
from app.repositories.in_memory import InMemoryReportRepository, ReportRecord
from app.repositories.supabase_repo import SupabaseReportRepository


def create_report_repository() -> InMemoryReportRepository:
    settings = get_settings()
    if (
        settings.storage_backend == "supabase"
        and settings.supabase_url
        and settings.supabase_service_role_key
    ):
        return SupabaseReportRepository(
            supabase_url=settings.supabase_url,
            service_role_key=settings.supabase_service_role_key,
        )
    return InMemoryReportRepository()


reports = create_report_repository()

__all__ = ["ReportRecord", "reports"]
