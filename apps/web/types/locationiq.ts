export type ReportRequestStatus =
  | "created"
  | "resolving_location"
  | "needs_pin_confirmation"
  | "preview_generating"
  | "preview_ready"
  | "checkout_created"
  | "payment_pending"
  | "paid"
  | "generation_queued"
  | "generating"
  | "completed"
  | "completed_with_data_gaps"
  | "failed"
  | "refunded"
  | "cancelled";

export type Pin = {
  latitude: number;
  longitude: number;
  address_text?: string | null;
  locality?: string | null;
  city?: string | null;
  district?: string | null;
  state?: string | null;
  pin_code?: string | null;
  plus_code?: string | null;
  geocode_quality_note?: string | null;
};

export type PurposeSummary = {
  purpose_category: string;
  sub_purpose: string;
  display_label: string;
};

export type LocationPreviewResponse = {
  report_request_id: string;
  report_token: string;
  status: ReportRequestStatus;
  pin: Pin;
  internal_location_profile: {
    s2_levels_available: string[];
    profile_status: string;
  };
  purpose: PurposeSummary;
  map: {
    provider: string;
    marker: {
      latitude: number;
      longitude: number;
    };
    nearby_context: Array<Record<string, unknown>>;
  };
};

export type ConfirmPreviewResponse = {
  report_request_id: string;
  report_token: string;
  status: ReportRequestStatus;
  preview: {
    headline: string;
    pin_summary: string;
    location_character_teaser: string;
    preview_points: string[];
    locked_sections: string[];
  };
  payment: {
    cta_label: string;
    amount_display: string;
  };
};

export type CheckoutResponse = {
  checkout_session_id: string;
  checkout_url?: string | null;
  provider: "mock" | "razorpay" | string;
  key_id?: string | null;
  order_id?: string | null;
  amount?: number | null;
  currency: string;
  amount_display?: string | null;
};

export type ReportStatusResponse = {
  report_id?: string | null;
  status: ReportRequestStatus;
  stage: string;
  progress_percent: number;
  message: string;
  eta_note: string;
};

export type ReportResponse = {
  report_id: string;
  status: ReportRequestStatus;
  report: Record<string, any>;
};
