from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class ReportRequestStatus(str, Enum):
    created = "created"
    resolving_location = "resolving_location"
    needs_pin_confirmation = "needs_pin_confirmation"
    preview_generating = "preview_generating"
    preview_ready = "preview_ready"
    checkout_created = "checkout_created"
    payment_pending = "payment_pending"
    paid = "paid"
    generation_queued = "generation_queued"
    generating = "generating"
    completed = "completed"
    completed_with_data_gaps = "completed_with_data_gaps"
    failed = "failed"
    refunded = "refunded"
    cancelled = "cancelled"


class WorkflowStage(str, Enum):
    resolving_location = "resolving_location"
    profiling_location = "profiling_location"
    planning_sources = "planning_sources"
    collecting_map_data = "collecting_map_data"
    collecting_access_data = "collecting_access_data"
    collecting_public_web = "collecting_public_web"
    collecting_official_data = "collecting_official_data"
    collecting_imagery = "collecting_imagery"
    normalizing_observations = "normalizing_observations"
    normalizing_prices = "normalizing_prices"
    generating_visuals = "generating_visuals"
    composing_report = "composing_report"
    validating_report = "validating_report"
    rendering_report = "rendering_report"
    emailing_report = "emailing_report"
    completed = "completed"
    failed = "failed"


class PaymentStatus(str, Enum):
    not_started = "not_started"
    checkout_created = "checkout_created"
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"
    chargeback = "chargeback"


class Pin(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    address_text: Optional[str] = None
    locality: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    geocode_quality_note: Optional[str] = None


class ConfirmedPin(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class LocationPreviewRequest(BaseModel):
    location_input: str = Field(min_length=1, max_length=2000)
    use_case_input: str = Field(min_length=1, max_length=500)
    email: EmailStr


class InternalLocationProfile(BaseModel):
    s2_levels_available: List[str]
    profile_status: str


class PurposeSummary(BaseModel):
    purpose_category: str
    sub_purpose: str
    display_label: str


class MapMarker(BaseModel):
    latitude: float
    longitude: float


class MapPreview(BaseModel):
    provider: str
    marker: MapMarker
    nearby_context: List[Dict[str, Any]] = Field(default_factory=list)


class LocationPreviewResponse(BaseModel):
    report_request_id: str
    report_token: str
    status: ReportRequestStatus
    pin: Pin
    internal_location_profile: InternalLocationProfile
    purpose: PurposeSummary
    map: MapPreview


class ConfirmPreviewRequest(BaseModel):
    confirmed_pin: ConfirmedPin


class PreviewContent(BaseModel):
    headline: str
    pin_summary: str
    location_character_teaser: str
    preview_points: List[str]
    locked_sections: List[str]


class PaymentPreview(BaseModel):
    cta_label: str
    amount_display: str


class ConfirmPreviewResponse(BaseModel):
    report_request_id: str
    report_token: str
    status: ReportRequestStatus
    preview: PreviewContent
    payment: PaymentPreview


class CheckoutRequest(BaseModel):
    success_url: str
    cancel_url: str


class CheckoutResponse(BaseModel):
    checkout_session_id: str
    checkout_url: Optional[str] = None
    provider: str = "mock"
    key_id: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[int] = None
    currency: str = "INR"
    amount_display: Optional[str] = None


class PaymentWebhookRequest(BaseModel):
    checkout_session_id: str
    payment_id: Optional[str] = None
    status: PaymentStatus = PaymentStatus.paid
    idempotency_key: str = Field(min_length=1)
    provider_payload: Dict[str, Any] = Field(default_factory=dict)
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature: Optional[str] = None


class ReportStatusResponse(BaseModel):
    report_id: Optional[str] = None
    status: ReportRequestStatus
    stage: WorkflowStage
    progress_percent: int = Field(ge=0, le=100)
    message: str
    eta_note: str


class ReportResponse(BaseModel):
    report_id: str
    status: ReportRequestStatus
    report: Dict[str, Any]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
