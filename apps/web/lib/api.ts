import type {
  CheckoutResponse,
  ConfirmPreviewResponse,
  LocationPreviewResponse,
  ReportResponse,
  ReportStatusResponse,
} from "@/types/locationiq";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    let message = `Request failed with ${response.status}`;
    try {
      const errorBody = await response.json();
      message =
        typeof errorBody.detail === "string"
          ? errorBody.detail
          : errorBody.detail?.message ?? message;
    } catch {
      // Keep the status-based message if the API did not return JSON.
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export async function createLocationPreview(payload: {
  location_input: string;
  use_case_input: string;
  email: string;
}) {
  return requestJson<LocationPreviewResponse>("/v1/location-preview", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function confirmPreview(reportRequestId: string, latitude: number, longitude: number) {
  return requestJson<ConfirmPreviewResponse>(
    `/v1/report-requests/${reportRequestId}/confirm-preview`,
    {
      method: "POST",
      body: JSON.stringify({
        confirmed_pin: {
          latitude,
          longitude,
        },
      }),
    },
  );
}

export async function createCheckout(reportRequestId: string) {
  const origin = typeof window !== "undefined" ? window.location.origin : "http://localhost:3000";
  return requestJson<CheckoutResponse>(`/v1/report-requests/${reportRequestId}/checkout`, {
    method: "POST",
    body: JSON.stringify({
      success_url: `${origin}/report/${reportRequestId}?payment=success`,
      cancel_url: `${origin}/preview/${reportRequestId}?payment=cancelled`,
    }),
  });
}

export async function completeMockPayment(checkoutSessionId: string) {
  return requestJson<{ ok: boolean; report_token: string; status: string }>("/v1/webhooks/payment", {
    method: "POST",
    body: JSON.stringify({
      checkout_session_id: checkoutSessionId,
      payment_id: `mock_pay_${Date.now()}`,
      status: "paid",
      idempotency_key: `mock_${checkoutSessionId}`,
      provider_payload: {
        mode: "local_development",
      },
    }),
  });
}

export async function completeRazorpayPayment(payload: {
  checkout_session_id: string;
  razorpay_order_id: string;
  razorpay_payment_id: string;
  razorpay_signature: string;
}) {
  return requestJson<{ ok: boolean; report_token: string; status: string }>("/v1/webhooks/payment", {
    method: "POST",
    body: JSON.stringify({
      checkout_session_id: payload.checkout_session_id,
      payment_id: payload.razorpay_payment_id,
      status: "paid",
      idempotency_key: payload.razorpay_payment_id,
      provider_payload: {
        provider: "razorpay",
      },
      razorpay_order_id: payload.razorpay_order_id,
      razorpay_payment_id: payload.razorpay_payment_id,
      razorpay_signature: payload.razorpay_signature,
    }),
  });
}

export async function getReportStatus(reportToken: string) {
  return requestJson<ReportStatusResponse>(`/v1/reports/${reportToken}/status`, {
    cache: "no-store",
  });
}

export async function getReport(reportToken: string) {
  return requestJson<ReportResponse>(`/v1/reports/${reportToken}`, {
    cache: "no-store",
  });
}
