from uuid import uuid4

import razorpay

from app.core.config import Settings


def create_mock_checkout_url(report_request_id: str) -> tuple:
    session_id = f"mock_cs_{uuid4().hex}"
    return session_id, f"http://localhost:3000/report/{report_request_id}/progress?mock_checkout={session_id}"


def create_razorpay_order(
    *,
    settings: Settings,
    report_request_id: str,
    email: str,
    purpose_label: str,
) -> dict:
    if not settings.razorpay_key_id or not settings.razorpay_key_secret:
        raise RuntimeError("Razorpay key id and secret are required for Razorpay checkout.")

    amount_paise = settings.report_price_inr * 100
    client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
    order = client.order.create(
        {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": report_request_id[:40],
            "notes": {
                "report_request_id": report_request_id,
                "email": email,
                "purpose": purpose_label,
            },
        }
    )
    return {
        "checkout_session_id": order["id"],
        "order_id": order["id"],
        "provider": "razorpay",
        "key_id": settings.razorpay_key_id,
        "amount": amount_paise,
        "currency": order.get("currency", "INR"),
        "amount_display": f"Rs {settings.report_price_inr:,}",
    }


def verify_razorpay_payment_signature(
    *,
    settings: Settings,
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
) -> None:
    client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
    client.utility.verify_payment_signature(
        {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }
    )
