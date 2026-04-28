import os

os.environ["LOCATIONIQ_PAYMENT_PROVIDER"] = "mock"
os.environ["LOCATIONIQ_STORAGE"] = "memory"

from fastapi.testclient import TestClient

from app.main import app


def test_no_login_report_lifecycle() -> None:
    client = TestClient(app)

    preview_response = client.post(
        "/v1/location-preview",
        json={
            "location_input": "18.576742, 73.736961",
            "use_case_input": "Open a pickleball facility",
            "email": "customer@example.com",
        },
    )
    assert preview_response.status_code == 200
    preview = preview_response.json()
    assert preview["status"] == "needs_pin_confirmation"
    assert preview["pin"]["latitude"] == 18.576742
    assert preview["purpose"]["sub_purpose"] == "pickleball_facility"

    report_request_id = preview["report_request_id"]
    token = preview["report_token"]

    confirm_response = client.post(
        f"/v1/report-requests/{report_request_id}/confirm-preview",
        json={"confirmed_pin": {"latitude": 18.576742, "longitude": 73.736961}},
    )
    assert confirm_response.status_code == 200
    assert confirm_response.json()["status"] == "preview_ready"

    checkout_response = client.post(
        f"/v1/report-requests/{report_request_id}/checkout",
        json={
            "success_url": "http://localhost:3000/success",
            "cancel_url": "http://localhost:3000/cancel",
        },
    )
    assert checkout_response.status_code == 200
    checkout_session_id = checkout_response.json()["checkout_session_id"]

    webhook_response = client.post(
        "/v1/webhooks/payment",
        json={
            "checkout_session_id": checkout_session_id,
            "payment_id": "pay_test",
            "status": "paid",
            "idempotency_key": "test-key",
            "provider_payload": {},
        },
    )
    assert webhook_response.status_code == 200

    status_response = client.get(f"/v1/reports/{token}/status")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "completed"

    report_response = client.get(f"/v1/reports/{token}")
    assert report_response.status_code == 200
    report = report_response.json()["report"]
    assert report["metadata"]["selected_pin"]["latitude"] == 18.576742
    assert "No buy/open/invest verdict" in report["purpose_lens"]["excluded_or_not_claimed"]
