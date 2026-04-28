from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from uuid import uuid4

from app.models import (
    PaymentStatus,
    Pin,
    PreviewContent,
    PurposeSummary,
    ReportRequestStatus,
    WorkflowStage,
    utc_now,
)


@dataclass
class ReportRecord:
    id: str
    public_token: str
    email: str
    location_input: str
    use_case_input: str
    purpose: PurposeSummary
    pin: Pin
    cell_profile: Dict[str, Any]
    status: ReportRequestStatus = ReportRequestStatus.needs_pin_confirmation
    payment_status: PaymentStatus = PaymentStatus.not_started
    current_stage: WorkflowStage = WorkflowStage.profiling_location
    progress_percent: int = 10
    preview: Optional[PreviewContent] = None
    checkout_session_id: Optional[str] = None
    report_id: Optional[str] = None
    report_json: Optional[Dict[str, Any]] = None
    webhook_idempotency_keys: set = field(default_factory=set)
    created_at: object = field(default_factory=utc_now)
    updated_at: object = field(default_factory=utc_now)


class InMemoryReportRepository:
    def __init__(self) -> None:
        self._by_id: Dict[str, ReportRecord] = {}
        self._by_token: Dict[str, str] = {}
        self._by_checkout: Dict[str, str] = {}

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
        record = ReportRecord(
            id=str(uuid4()),
            public_token=f"rt_{uuid4().hex}",
            email=email,
            location_input=location_input,
            use_case_input=use_case_input,
            purpose=purpose,
            pin=pin,
            cell_profile=cell_profile,
        )
        self._by_id[record.id] = record
        self._by_token[record.public_token] = record.id
        return record

    def get(self, report_request_id: str) -> Optional[ReportRecord]:
        return self._by_id.get(report_request_id)

    def get_by_token(self, public_token: str) -> Optional[ReportRecord]:
        report_request_id = self._by_token.get(public_token)
        if report_request_id is None:
            return None
        return self.get(report_request_id)

    def get_by_checkout(self, checkout_session_id: str) -> Optional[ReportRecord]:
        report_request_id = self._by_checkout.get(checkout_session_id)
        if report_request_id is None:
            return None
        return self.get(report_request_id)

    def save(self, record: ReportRecord) -> ReportRecord:
        record.updated_at = utc_now()
        self._by_id[record.id] = record
        self._by_token[record.public_token] = record.id
        if record.checkout_session_id:
            self._by_checkout[record.checkout_session_id] = record.id
        return record

