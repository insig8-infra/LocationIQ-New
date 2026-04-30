"use client";

import { FormEvent, useMemo, useState } from "react";
import { ExactPinMap } from "@/components/ExactPinMap";
import { ReportView } from "@/components/ReportView";
import {
  completeRazorpayPayment,
  completeMockPayment,
  confirmPreview,
  createCheckout,
  createLocationPreview,
  getReport,
  getReportStatus,
} from "@/lib/api";
import type {
  CheckoutResponse,
  ConfirmPreviewResponse,
  LocationPreviewResponse,
  ReportResponse,
  ReportStatusResponse,
} from "@/types/locationiq";

type FlowStep = "input" | "confirm" | "preview" | "payment" | "progress" | "report";

declare global {
  interface Window {
    Razorpay?: new (options: RazorpayOptions) => { open: () => void };
  }
}

type RazorpayOptions = {
  key: string;
  amount: number;
  currency: string;
  name: string;
  description: string;
  order_id: string;
  prefill: {
    email: string;
  };
  handler: (response: {
    razorpay_order_id: string;
    razorpay_payment_id: string;
    razorpay_signature: string;
  }) => void;
};

const useCaseChips = [
  "Buy or rent a home",
  "Cafe / restaurant / cloud kitchen",
  "Sports facility",
  "Gym / fitness studio",
  "Franchise / storefront",
];

export default function Home() {
  const [step, setStep] = useState<FlowStep>("input");
  const [locationInput, setLocationInput] = useState("18.576742, 73.736961");
  const [useCaseInput, setUseCaseInput] = useState("Open a pickleball facility");
  const [email, setEmail] = useState("");
  const [locationPreview, setLocationPreview] = useState<LocationPreviewResponse | null>(null);
  const [preview, setPreview] = useState<ConfirmPreviewResponse | null>(null);
  const [checkout, setCheckout] = useState<CheckoutResponse | null>(null);
  const [status, setStatus] = useState<ReportStatusResponse | null>(null);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [isBusy, setIsBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const progress = useMemo(() => {
    if (status) return status.progress_percent;
    if (step === "input") return 0;
    if (step === "confirm") return 18;
    if (step === "preview") return 34;
    if (step === "payment") return 52;
    if (step === "progress") return 78;
    return 100;
  }, [status, step]);

  async function runAction(action: () => Promise<void>) {
    setIsBusy(true);
    setError(null);
    try {
      await action();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Something went wrong.");
    } finally {
      setIsBusy(false);
    }
  }

  async function submitLocation(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await runAction(async () => {
      const nextPreview = await createLocationPreview({
        location_input: locationInput,
        use_case_input: useCaseInput,
        email,
      });
      setLocationPreview(nextPreview);
      setStep("confirm");
    });
  }

  async function confirmPin() {
    if (!locationPreview) return;
    await runAction(async () => {
      const nextPreview = await confirmPreview(
        locationPreview.report_request_id,
        locationPreview.pin.latitude,
        locationPreview.pin.longitude,
      );
      setPreview(nextPreview);
      setStep("preview");
    });
  }

  async function startCheckout() {
    if (!locationPreview) return;
    await runAction(async () => {
      const nextCheckout = await createCheckout(
        locationPreview.report_request_id,
        locationPreview.report_token,
      );
      setCheckout(nextCheckout);
      setStep("payment");
    });
  }

  async function completePayment() {
    if (!checkout || !locationPreview) return;
    await runAction(async () => {
      setStep("progress");
      const payment = await completeMockPayment(checkout.checkout_session_id);
      const nextStatus = await getReportStatus(payment.report_token);
      const nextReport = await getReport(payment.report_token);
      setStatus(nextStatus);
      setReport(nextReport);
      setStep("report");
    });
  }

  async function payWithRazorpay() {
    if (!checkout || !locationPreview || !checkout.key_id || !checkout.order_id || !checkout.amount) {
      setError("Razorpay checkout is missing order data.");
      return;
    }

    await runAction(async () => {
      await loadRazorpayScript();
      if (!window.Razorpay) {
        throw new Error("Razorpay Checkout could not be loaded.");
      }

      await new Promise<void>((resolve, reject) => {
        const razorpay = new window.Razorpay!({
          key: checkout.key_id!,
          amount: checkout.amount!,
          currency: checkout.currency,
          name: "LocationIQ",
          description: `Location report for ${locationPreview.purpose.display_label}`,
          order_id: checkout.order_id!,
          prefill: {
            email,
          },
          handler: async (response) => {
            try {
              setStep("progress");
              const payment = await completeRazorpayPayment({
                checkout_session_id: checkout.checkout_session_id,
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
              });
              const nextStatus = await getReportStatus(payment.report_token);
              const nextReport = await getReport(payment.report_token);
              setStatus(nextStatus);
              setReport(nextReport);
              setStep("report");
              resolve();
            } catch (caught) {
              reject(caught);
            }
          },
        });
        razorpay.open();
      });
    });
  }

  const pin = locationPreview?.pin;

  return (
    <main className="app-shell">
      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">LocationIQ</p>
            <h1>Location report request</h1>
          </div>
          <div className="stage-meter" aria-label="Flow progress">
            <span style={{ width: `${progress}%` }} />
          </div>
        </header>

        <div className="flow-grid">
          <section className="input-panel">
            <form onSubmit={submitLocation}>
              <div className="field">
                <label htmlFor="location">Location</label>
                <input
                  id="location"
                  value={locationInput}
                  onChange={(event) => setLocationInput(event.target.value)}
                  placeholder="18.576742, 73.736961"
                  required
                />
              </div>

              <div className="field">
                <label>Use case</label>
                <div className="chip-row">
                  {useCaseChips.map((chip) => (
                    <button
                      className={useCaseInput === chip ? "chip selected" : "chip"}
                      key={chip}
                      type="button"
                      onClick={() => setUseCaseInput(chip)}
                    >
                      {chip}
                    </button>
                  ))}
                </div>
                <input
                  value={useCaseInput}
                  onChange={(event) => setUseCaseInput(event.target.value)}
                  placeholder="Open a pickleball facility"
                  required
                />
              </div>

              <div className="field">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="you@example.com"
                  type="email"
                  required
                />
              </div>

              <button className="primary-button" disabled={isBusy} type="submit">
                {isBusy && step === "input" ? "Checking..." : "Check Location"}
              </button>
            </form>
          </section>

          <section className="map-panel" aria-label="Exact pin map preview">
            <ExactPinMap pin={pin} />
          </section>
        </div>

        {error ? <div className="error-panel">{error}</div> : null}

        {step === "confirm" && locationPreview ? (
          <section className="action-band">
            <div>
              <p className="eyebrow">Pin confirmation</p>
              <h2>{formatPin(locationPreview.pin)}</h2>
              <p>{locationPreview.pin.geocode_quality_note}</p>
            </div>
            <button className="primary-button" disabled={isBusy} onClick={confirmPin}>
              Confirm and Analyse
            </button>
          </section>
        ) : null}

        {step === "preview" && preview ? (
          <section className="preview-panel">
            <div className="section-heading">
              <p className="eyebrow">Low-cost preview</p>
              <h2>{preview.preview.headline}</h2>
              <p>{preview.preview.pin_summary}</p>
            </div>
            <div className="preview-grid">
              <div className="summary-panel">
                <h3>Location character</h3>
                <p>{preview.preview.location_character_teaser}</p>
              </div>
              <div className="summary-panel">
                <h3>Full report checks</h3>
                <ul>
                  {preview.preview.preview_points.map((point) => (
                    <li key={point}>{point}</li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="locked-grid">
              {preview.preview.locked_sections.map((section) => (
                <span key={section}>{section}</span>
              ))}
            </div>
            <button className="primary-button" disabled={isBusy} onClick={startCheckout}>
              {preview.payment.cta_label} - {preview.payment.amount_display}
            </button>
          </section>
        ) : null}

        {step === "payment" && checkout ? (
          <section className="action-band">
            <div>
              <p className="eyebrow">Payment</p>
              <h2>{checkout.provider === "razorpay" ? "Razorpay checkout is ready" : "Mock checkout is ready"}</h2>
              <p>
                {checkout.provider === "razorpay" ? "Order" : "Session"} {checkout.checkout_session_id}
              </p>
            </div>
            {checkout.provider === "razorpay" ? (
              <button className="primary-button" disabled={isBusy} onClick={payWithRazorpay}>
                Pay with Razorpay
              </button>
            ) : (
              <button className="primary-button" disabled={isBusy} onClick={completePayment}>
                Complete Mock Payment
              </button>
            )}
          </section>
        ) : null}

        {step === "progress" ? (
          <section className="action-band">
            <div>
              <p className="eyebrow">Progress</p>
              <h2>{status?.message ?? "Generating the report"}</h2>
              <p>{status?.eta_note ?? "The report will open here when ready."}</p>
            </div>
            <div className="status-number">{progress}%</div>
          </section>
        ) : null}

        {step === "report" && report ? (
          <ReportView report={report} reportToken={locationPreview?.report_token} />
        ) : null}
      </section>
    </main>
  );
}

function formatPin(pin: { latitude: number; longitude: number }) {
  return `${pin.latitude.toFixed(6)}, ${pin.longitude.toFixed(6)}`;
}

function loadRazorpayScript() {
  return new Promise<void>((resolve, reject) => {
    if (window.Razorpay) {
      resolve();
      return;
    }

    const existingScript = document.querySelector<HTMLScriptElement>(
      'script[src="https://checkout.razorpay.com/v1/checkout.js"]',
    );
    if (existingScript) {
      existingScript.addEventListener("load", () => resolve(), { once: true });
      existingScript.addEventListener("error", () => reject(new Error("Razorpay script failed.")), {
        once: true,
      });
      return;
    }

    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Razorpay script failed."));
    document.body.appendChild(script);
  });
}
