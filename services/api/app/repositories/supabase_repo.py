from typing import Any, Dict, Optional

from supabase import Client, create_client

from app.models import (
    PaymentStatus,
    Pin,
    PreviewContent,
    PurposeSummary,
    ReportRequestStatus,
    WorkflowStage,
)
from app.repositories.in_memory import InMemoryReportRepository, ReportRecord


class SupabaseReportRepository(InMemoryReportRepository):
    """Supabase-backed repository with in-memory caching for active local requests."""

    def __init__(self, *, supabase_url: str, service_role_key: str) -> None:
        super().__init__()
        self.client: Client = create_client(supabase_url, service_role_key)

    def create(
        self,
        *,
        email: str,
        location_input: str,
        use_case_input: str,
        purpose: PurposeSummary,
        pin: Pin,
        cell_profile: Dict[str, Any],
    ) -> ReportRecord:
        request_row = (
            self.client.table("report_requests")
            .insert(
                {
                    "email": email,
                    "location_input": location_input,
                    "use_case_input": use_case_input,
                    "purpose_category": purpose.purpose_category,
                    "sub_purpose": purpose.sub_purpose,
                    "selected_context": {},
                    "status": ReportRequestStatus.needs_pin_confirmation.value,
                    "payment_status": PaymentStatus.not_started.value,
                    "current_stage": WorkflowStage.profiling_location.value,
                    "progress_percent": 10,
                }
            )
            .execute()
            .data[0]
        )

        cells = cell_profile.get("cells", {})
        location_row = (
            self.client.table("locations").insert(
                {
                    "report_request_id": request_row["id"],
                    "selected_latitude": pin.latitude,
                    "selected_longitude": pin.longitude,
                    "geom": f"POINT({pin.longitude} {pin.latitude})",
                    "address_text": pin.address_text,
                    "locality": pin.locality,
                    "city": pin.city,
                    "district": pin.district,
                    "state": pin.state,
                    "pin_code": pin.pin_code,
                    "plus_code": pin.plus_code,
                    "geocode_quality_note": pin.geocode_quality_note,
                    "pin_identity_state": "coordinate_confirmed",
                    "s2_l12_cell_id": cells.get("L12"),
                    "s2_l13_cell_id": cells.get("L13"),
                    "s2_l14_cell_id": cells.get("L14"),
                    "s2_l15_cell_id": cells.get("L15"),
                    "s2_l16_cell_id": cells.get("L16"),
                }
            )
            .execute()
            .data[0]
        )

        reverse_rows = []
        for result in cell_profile.get("reverse_geocode_results", []):
            reverse_rows.append(
                {
                    "location_id": location_row["id"],
                    "provider": result.get("provider", "unknown"),
                    "provider_place_id": result.get("provider_place_id"),
                    "response_json": result.get("response_json", {}),
                    "resolved_latitude": result.get("resolved_latitude"),
                    "resolved_longitude": result.get("resolved_longitude"),
                    "distance_from_selected_m": result.get("distance_from_selected_m"),
                    "cache_policy": result.get("cache_policy"),
                }
            )
        if reverse_rows:
            self.client.table("reverse_geocode_results").insert(reverse_rows).execute()

        record = ReportRecord(
            id=request_row["id"],
            public_token=request_row["public_token"],
            email=email,
            location_input=location_input,
            use_case_input=use_case_input,
            purpose=purpose,
            pin=pin,
            cell_profile=cell_profile,
        )
        return super().save(record)

    def get(self, report_request_id: str) -> Optional[ReportRecord]:
        cached = super().get(report_request_id)
        if cached is not None:
            return cached

        rows = (
            self.client.table("report_requests")
            .select("*")
            .eq("id", report_request_id)
            .limit(1)
            .execute()
            .data
        )
        if not rows:
            return None
        return self._hydrate(rows[0])

    def get_by_token(self, public_token: str) -> Optional[ReportRecord]:
        cached = super().get_by_token(public_token)
        if cached is not None:
            return cached

        rows = (
            self.client.table("report_requests")
            .select("*")
            .eq("public_token", public_token)
            .limit(1)
            .execute()
            .data
        )
        if not rows:
            return None
        return self._hydrate(rows[0])

    def get_by_checkout(self, checkout_session_id: str) -> Optional[ReportRecord]:
        cached = super().get_by_checkout(checkout_session_id)
        if cached is not None:
            return cached

        payment_rows = (
            self.client.table("payments")
            .select("report_request_id")
            .eq("checkout_session_id", checkout_session_id)
            .limit(1)
            .execute()
            .data
        )
        if not payment_rows:
            return None
        return self.get(payment_rows[0]["report_request_id"])

    def save(self, record: ReportRecord) -> ReportRecord:
        self.client.table("report_requests").update(
            {
                "status": record.status.value,
                "payment_status": record.payment_status.value,
                "current_stage": record.current_stage.value,
                "progress_percent": record.progress_percent,
            }
        ).eq("id", record.id).execute()

        if record.preview is not None:
            self.client.table("previews").upsert(
                {
                    "report_request_id": record.id,
                    "preview_json": record.preview.model_dump(mode="json"),
                    "cost_class": "low_cost",
                },
                on_conflict="report_request_id",
            ).execute()

        if record.checkout_session_id is not None:
            self.client.table("payments").upsert(
                {
                    "report_request_id": record.id,
                    "provider": "razorpay"
                    if record.checkout_session_id.startswith("order_")
                    else "mock",
                    "checkout_session_id": record.checkout_session_id,
                    "amount": None,
                    "currency": "INR",
                    "status": record.payment_status.value,
                },
                on_conflict="checkout_session_id",
            ).execute()

        if record.report_id is not None and record.report_json is not None:
            self.client.table("reports").upsert(
                {
                    "report_request_id": record.id,
                    "public_token": record.public_token,
                    "schema_version": "interpretive-location-report.v4",
                    "report_json": record.report_json,
                    "status": record.status.value,
                },
                on_conflict="public_token",
            ).execute()

        return super().save(record)

    def _hydrate(self, row: Dict[str, Any]) -> ReportRecord:
        location_rows = (
            self.client.table("locations")
            .select("*")
            .eq("report_request_id", row["id"])
            .limit(1)
            .execute()
            .data
        )
        location = location_rows[0] if location_rows else {}
        pin = Pin(
            latitude=float(location.get("selected_latitude") or 0),
            longitude=float(location.get("selected_longitude") or 0),
            address_text=location.get("address_text"),
            locality=location.get("locality"),
            city=location.get("city"),
            state=location.get("state"),
            geocode_quality_note=location.get("geocode_quality_note"),
        )
        purpose = PurposeSummary(
            purpose_category=row.get("purpose_category") or "general_location_read",
            sub_purpose=row.get("sub_purpose") or "custom_use_case",
            display_label=row.get("use_case_input") or "Custom use case",
        )
        cell_profile = {
            "cells": {
                "L12": location.get("s2_l12_cell_id"),
                "L13": location.get("s2_l13_cell_id"),
                "L14": location.get("s2_l14_cell_id"),
                "L15": location.get("s2_l15_cell_id"),
                "L16": location.get("s2_l16_cell_id"),
            },
            "profile_status": "generated",
            "preview_safe_summary": (
                "The exact coordinate has been converted into multi-resolution location cells."
            ),
        }
        record = ReportRecord(
            id=row["id"],
            public_token=row["public_token"],
            email=row["email"],
            location_input=row["location_input"],
            use_case_input=row["use_case_input"],
            purpose=purpose,
            pin=pin,
            cell_profile=cell_profile,
            status=ReportRequestStatus(row["status"]),
            payment_status=PaymentStatus(row["payment_status"]),
            current_stage=WorkflowStage(row["current_stage"] or WorkflowStage.profiling_location),
            progress_percent=row["progress_percent"],
        )

        preview_rows = (
            self.client.table("previews")
            .select("preview_json")
            .eq("report_request_id", row["id"])
            .limit(1)
            .execute()
            .data
        )
        if preview_rows:
            record.preview = PreviewContent.model_validate(preview_rows[0]["preview_json"])

        payment_rows = (
            self.client.table("payments")
            .select("checkout_session_id")
            .eq("report_request_id", row["id"])
            .limit(1)
            .execute()
            .data
        )
        if payment_rows:
            record.checkout_session_id = payment_rows[0]["checkout_session_id"]

        report_rows = (
            self.client.table("reports")
            .select("id, report_json")
            .eq("report_request_id", row["id"])
            .limit(1)
            .execute()
            .data
        )
        if report_rows:
            record.report_id = report_rows[0]["id"]
            record.report_json = report_rows[0]["report_json"]

        return super().save(record)
