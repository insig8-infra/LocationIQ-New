from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.models import (
    CheckoutRequest,
    CheckoutResponse,
    ConfirmPreviewRequest,
    ConfirmPreviewResponse,
    InternalLocationProfile,
    LocationPreviewRequest,
    LocationPreviewResponse,
    MapMarker,
    MapPreview,
    PaymentPreview,
    PaymentStatus,
    PaymentWebhookRequest,
    ReportRequestStatus,
    ReportResponse,
    ReportStatusResponse,
    WorkflowStage,
)
from app.repositories import ReportRecord, reports
from app.services.checkout_service import (
    create_mock_checkout_url,
    create_razorpay_order,
    verify_razorpay_payment_signature,
)
from app.services.location_resolver import build_cell_profile, resolve_location, s2_levels_available
from app.services.preview_generator import generate_preview
from app.services.purpose_planner import infer_purpose
from app.services.report_generator import generate_demo_report


router = APIRouter(prefix="/v1", tags=["report requests"])


def get_record_or_404(report_request_id: str) -> ReportRecord:
    record = reports.get(report_request_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report request not found")
    return record


def get_record_by_token_or_404(report_token: str) -> ReportRecord:
    record = reports.get_by_token(report_token)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return record


def nearby_context_from_profile(cell_profile: dict) -> list:
    context = []
    for result in cell_profile.get("reverse_geocode_results", []):
        if result.get("collection_type") == "provider_error":
            continue
        context.append(
            {
                "provider": result.get("provider"),
                "address_text": result.get("address_text"),
                "locality": result.get("locality"),
                "city": result.get("city"),
                "state": result.get("state"),
                "distance_from_selected_m": result.get("distance_from_selected_m"),
                "note": result.get("user_facing_source_note"),
            }
        )
    return context


@router.post("/location-preview", response_model=LocationPreviewResponse)
async def create_location_preview(payload: LocationPreviewRequest) -> LocationPreviewResponse:
    purpose = infer_purpose(payload.use_case_input)
    pin, cell_profile = resolve_location(payload.location_input)
    record = reports.create(
        email=str(payload.email),
        location_input=payload.location_input,
        use_case_input=payload.use_case_input,
        purpose=purpose,
        pin=pin,
        cell_profile=cell_profile,
    )
    return LocationPreviewResponse(
        report_request_id=record.id,
        report_token=record.public_token,
        status=record.status,
        pin=pin,
        internal_location_profile=InternalLocationProfile(
            s2_levels_available=s2_levels_available(cell_profile),
            profile_status=cell_profile["profile_status"],
        ),
        purpose=purpose,
        map=MapPreview(
            provider="google_maps",
            marker=MapMarker(latitude=pin.latitude, longitude=pin.longitude),
            nearby_context=nearby_context_from_profile(cell_profile),
        ),
    )


@router.post(
    "/report-requests/{report_request_id}/confirm-preview",
    response_model=ConfirmPreviewResponse,
)
async def confirm_preview(
    report_request_id: str,
    payload: ConfirmPreviewRequest,
) -> ConfirmPreviewResponse:
    record = get_record_or_404(report_request_id)
    record.pin.latitude = payload.confirmed_pin.latitude
    record.pin.longitude = payload.confirmed_pin.longitude
    record.cell_profile = build_cell_profile(
        payload.confirmed_pin.latitude,
        payload.confirmed_pin.longitude,
    )
    record.status = ReportRequestStatus.preview_generating
    record.current_stage = WorkflowStage.profiling_location
    record.progress_percent = 20

    record.preview = generate_preview(
        record.pin,
        record.purpose,
        record.cell_profile["preview_safe_summary"],
    )
    record.status = ReportRequestStatus.preview_ready
    record.progress_percent = 30
    reports.save(record)

    settings = get_settings()
    return ConfirmPreviewResponse(
        report_request_id=record.id,
        report_token=record.public_token,
        status=record.status,
        preview=record.preview,
        payment=PaymentPreview(
            cta_label="Get Full Report",
            amount_display=f"Rs {settings.report_price_inr:,}",
        ),
    )


@router.post("/report-requests/{report_request_id}/checkout", response_model=CheckoutResponse)
async def create_checkout(
    report_request_id: str,
    payload: CheckoutRequest,
) -> CheckoutResponse:
    record = get_record_or_404(report_request_id)
    if record.status != ReportRequestStatus.preview_ready:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Preview must be ready before checkout.",
        )

    settings = get_settings()
    if settings.payment_provider == "razorpay":
        try:
            checkout_data = create_razorpay_order(
                settings=settings,
                report_request_id=record.id,
                email=record.email,
                purpose_label=record.purpose.display_label,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Razorpay order creation failed: {exc}",
            ) from exc

        record.checkout_session_id = checkout_data["checkout_session_id"]
        record.status = ReportRequestStatus.checkout_created
        record.payment_status = PaymentStatus.checkout_created
        reports.save(record)
        return CheckoutResponse(**checkout_data)

    session_id, checkout_url = create_mock_checkout_url(report_request_id)
    record.checkout_session_id = session_id
    record.status = ReportRequestStatus.checkout_created
    record.payment_status = PaymentStatus.checkout_created
    reports.save(record)
    return CheckoutResponse(
        checkout_session_id=session_id,
        checkout_url=checkout_url,
        provider="mock",
        order_id=session_id,
        amount=settings.report_price_inr * 100,
        amount_display=f"Rs {settings.report_price_inr:,}",
    )


@router.post("/webhooks/payment")
async def payment_webhook(payload: PaymentWebhookRequest) -> dict:
    record = reports.get_by_checkout(payload.checkout_session_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checkout session not found")

    if payload.idempotency_key in record.webhook_idempotency_keys:
        return {"ok": True, "idempotent": True, "report_token": record.public_token}

    record.webhook_idempotency_keys.add(payload.idempotency_key)
    if payload.status != PaymentStatus.paid:
        record.payment_status = payload.status
        record.status = ReportRequestStatus.failed
        record.current_stage = WorkflowStage.failed
        reports.save(record)
        return {"ok": True, "status": record.status}

    settings = get_settings()
    if record.checkout_session_id and record.checkout_session_id.startswith("order_"):
        if not (
            payload.razorpay_order_id
            and payload.razorpay_payment_id
            and payload.razorpay_signature
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Razorpay payment signature fields are required.",
            )
        try:
            verify_razorpay_payment_signature(
                settings=settings,
                razorpay_order_id=payload.razorpay_order_id,
                razorpay_payment_id=payload.razorpay_payment_id,
                razorpay_signature=payload.razorpay_signature,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Razorpay payment signature verification failed.",
            ) from exc

    record.payment_status = PaymentStatus.paid
    record.status = ReportRequestStatus.generating
    record.current_stage = WorkflowStage.composing_report
    record.progress_percent = 82
    record.report_id = f"rep_{record.id.replace('-', '')[:16]}"
    record.report_json = generate_demo_report(
        report_id=record.report_id,
        location_input=record.location_input,
        pin=record.pin,
        purpose=record.purpose,
    )
    record.status = ReportRequestStatus.completed
    record.current_stage = WorkflowStage.completed
    record.progress_percent = 100
    reports.save(record)
    return {"ok": True, "report_token": record.public_token, "status": record.status}


@router.get("/reports/{report_token}/status", response_model=ReportStatusResponse)
async def get_report_status(report_token: str) -> ReportStatusResponse:
    record = get_record_by_token_or_404(report_token)
    messages = {
        WorkflowStage.profiling_location: "Building the low-cost location profile.",
        WorkflowStage.composing_report: "Writing your location report.",
        WorkflowStage.completed: "Report ready.",
        WorkflowStage.failed: "The report could not be completed automatically.",
    }
    return ReportStatusResponse(
        report_id=record.report_id,
        status=record.status,
        stage=record.current_stage,
        progress_percent=record.progress_percent,
        message=messages.get(record.current_stage, "Working on your report."),
        eta_note="This can take a few minutes. We will email you when the report is ready.",
    )


@router.get("/reports/{report_token}", response_model=ReportResponse)
async def get_report(report_token: str) -> ReportResponse:
    record = get_record_by_token_or_404(report_token)
    if record.report_json is None or record.report_id is None:
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail="Report is not ready yet")
    return ReportResponse(
        report_id=record.report_id,
        status=record.status,
        report=record.report_json,
    )
