# LocationIQ API And Data Model Specification

Version: 0.1  
Date: April 25, 2026  
Status: Build-start draft

## 1. Scope

This document defines the first build API and Supabase data model for the no-login paid report flow.

The customer flow is:

```text
enter location + use case + email
resolve pin
confirm and analyse
show preview
pay
generate full report
show progress
render report
email report link
download PDF when available
```

## 2. Architecture Assumptions

| Area | Decision |
|---|---|
| Frontend | Next.js + React + TypeScript |
| Backend | FastAPI + Python |
| Database | Supabase Postgres + PostGIS + pgvector |
| Storage | Supabase Storage for artifacts if suitable; S3-compatible storage acceptable for heavier raw artifacts |
| Async workflow | Temporal |
| Browser automation | Playwright |
| Maps | Google Maps |
| LLM | OpenAI GPT-5.5 with extra high reasoning as default |
| Customer auth | No login |
| Customer identity | Email + secure report token |
| Payment | Payment provider checkout session |
| Admin auth | Separate admin access, required before scale |

## 3. Public API Endpoints

Base path:

```text
/v1
```

### 3.1 Create Lead / Resolve Pin

```http
POST /v1/location-preview
```

Purpose:

- Accept location, use case, and email.
- Resolve the pin.
- Return map preview data.
- Create an unpaid report request.

Request:

```json
{
  "location_input": "https://maps.app.goo.gl/T5bHbKyUutUAnXpP7",
  "use_case_input": "Set up a pickleball facility",
  "email": "customer@example.com"
}
```

Response:

```json
{
  "report_request_id": "rr_123",
  "status": "needs_pin_confirmation",
  "pin": {
    "latitude": 18.576742,
    "longitude": 73.736961,
    "address_text": "Near Hinjawadi, Pune, Maharashtra",
    "locality": "Hinjawadi",
    "city": "Pune",
    "state": "Maharashtra",
    "geocode_quality_note": "The coordinate is precise; nearby named places are shown only for orientation."
  },
  "internal_location_profile": {
    "s2_levels_available": ["L12", "L13", "L14", "L15", "L16"],
    "profile_status": "generated"
  },
  "purpose": {
    "purpose_category": "fitness_sports_site",
    "sub_purpose": "pickleball_facility",
    "display_label": "Pickleball facility"
  },
  "map": {
    "provider": "google_maps",
    "marker": { "latitude": 18.576742, "longitude": 73.736961 },
    "nearby_context": []
  }
}
```

Errors:

- `location_unresolved`
- `email_invalid`
- `unsupported_use_case`
- `ambiguous_location`

### 3.2 Confirm Pin And Generate Preview

```http
POST /v1/report-requests/{report_request_id}/confirm-preview
```

Purpose:

- Confirm exact pin.
- Generate low-cost preview.

Request:

```json
{
  "confirmed_pin": {
    "latitude": 18.576742,
    "longitude": 73.736961
  }
}
```

Response:

```json
{
  "report_request_id": "rr_123",
  "status": "preview_ready",
  "preview": {
    "headline": "Location preview for a pickleball facility near Hinjawadi",
    "pin_summary": "This report will analyse the exact coordinate, not the nearest named POI.",
    "location_character_teaser": "The mapped built-environment pattern around this pin looks mixed-use, with sports and food-support signals nearby. The full report will check whether that broader pattern applies to the exact pin.",
    "preview_points": [
      "The full report will check nearby sports operators, booking surfaces, and travel-time access.",
      "It will separate exact-pin context from broader Hinjawadi locality signals.",
      "Visible prices will only be compared if slot duration and unit can be normalized."
    ],
    "locked_sections": [
      "Exact pin and plot read",
      "Catchment and access",
      "Competition and pricing",
      "Spend and convenience",
      "Visual evidence pack"
    ]
  },
  "payment": {
    "cta_label": "Get Full Report",
    "amount_display": "TBD"
  }
}
```

### 3.3 Create Checkout

```http
POST /v1/report-requests/{report_request_id}/checkout
```

Purpose:

- Create payment checkout session.

Request:

```json
{
  "success_url": "https://locationiq.app/report/rr_123?payment=success",
  "cancel_url": "https://locationiq.app/preview/rr_123?payment=cancelled"
}
```

Response:

```json
{
  "checkout_session_id": "cs_123",
  "checkout_url": "https://payment-provider.example/checkout/cs_123"
}
```

### 3.4 Payment Webhook

```http
POST /v1/webhooks/payment
```

Purpose:

- Receive payment success/failure.
- Idempotently mark report request as paid.
- Start full report workflow.

Important:

- Verify webhook signature.
- Use idempotency key.
- Never trust client-side payment success alone.

### 3.5 Get Report Status

```http
GET /v1/reports/{report_token}/status
```

Response:

```json
{
  "report_id": "rep_123",
  "status": "generating",
  "stage": "collecting_public_web",
  "progress_percent": 42,
  "message": "Checking public platforms around the selected location.",
  "eta_note": "This can take a few minutes. We will email you when the report is ready."
}
```

### 3.6 Report Progress Stream

```http
GET /v1/reports/{report_token}/events
```

Use Server-Sent Events.

Event:

```json
{
  "stage": "normalizing_prices",
  "message": "Normalizing visible slot prices.",
  "progress_percent": 58,
  "timestamp": "2026-04-25T19:00:00+05:30"
}
```

### 3.7 Get Completed Report

```http
GET /v1/reports/{report_token}
```

Response:

```json
{
  "report_id": "rep_123",
  "status": "completed",
  "report": {
    "metadata": {},
    "reader_summary": {},
    "purpose_lens": {},
    "exact_pin": {},
    "multi_anchor_story": [],
    "catchment_and_reach": [],
    "arrival_reality": {},
    "key_numbers": [],
    "competition_and_pricing": {},
    "spend_and_convenience": {},
    "locality_conditions": [],
    "visual_evidence_pack": [],
    "field_verification_plan": [],
    "source_notes": []
  }
}
```

The `report` object must validate against:

```text
report-templates/output-schema.json
```

### 3.8 Download PDF

```http
GET /v1/reports/{report_token}/export.pdf
```

V1 can return:

- `202 Accepted` if PDF generation is pending.
- `302` to signed URL if ready.
- `501 Not Implemented` until PDF launch if interactive report launches first.

### 3.9 Support Retry

```http
POST /v1/admin/report-requests/{report_request_id}/retry
```

Admin only.

## 4. Status Enums

### 4.1 Report Request Status

```text
created
resolving_location
needs_pin_confirmation
preview_generating
preview_ready
checkout_created
payment_pending
paid
generation_queued
generating
completed
completed_with_data_gaps
failed
refunded
cancelled
```

### 4.2 Workflow Stage

```text
resolving_location
profiling_location
planning_sources
collecting_map_data
collecting_access_data
collecting_public_web
collecting_official_data
collecting_imagery
normalizing_observations
normalizing_prices
generating_visuals
composing_report
validating_report
rendering_report
emailing_report
completed
failed
```

### 4.3 Payment Status

```text
not_started
checkout_created
pending
paid
failed
refunded
chargeback
```

## 5. Supabase Data Model

Supabase extensions:

```sql
create extension if not exists postgis;
create extension if not exists vector;
create extension if not exists pgcrypto;
```

### 5.1 `report_requests`

Purpose:

- Central lifecycle record for preview, payment, generation, and delivery.

Columns:

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk | Generated server-side. |
| `public_token` | text unique | Secure unguessable report access token. |
| `email` | text | Customer email. |
| `location_input` | text | Raw input. |
| `use_case_input` | text | Raw use-case text/chip. |
| `purpose_category` | text | Normalized category. |
| `sub_purpose` | text | Normalized sub-purpose. |
| `selected_context` | jsonb | Inferred/default context, not user questionnaire. |
| `status` | text | Report request status enum. |
| `payment_status` | text | Payment status enum. |
| `current_stage` | text | Workflow stage enum. |
| `progress_percent` | int | 0-100. |
| `created_at` | timestamptz |  |
| `updated_at` | timestamptz |  |

### 5.2 `report_locations`

The implementation uses `report_locations` rather than a generic `locations` table name to avoid collisions in existing Supabase projects.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `selected_latitude` | numeric | Exact selected coordinate. |
| `selected_longitude` | numeric | Exact selected coordinate. |
| `geom` | geography(Point, 4326) | Exact selected pin. |
| `address_text` | text | Normalized display address. |
| `locality` | text |  |
| `city` | text |  |
| `district` | text |  |
| `state` | text |  |
| `pin_code` | text |  |
| `plus_code` | text |  |
| `digipin` | text |  |
| `geocode_quality_note` | text | Natural language note. |
| `pin_identity_state` | text | e.g. `coordinate_confirmed`. |
| `s2_l12_cell_id` | text | Broader built-environment context. |
| `s2_l13_cell_id` | text | Locality submarket context. |
| `s2_l14_cell_id` | text | Walkable/local pocket context. |
| `s2_l15_cell_id` | text | Near-neighborhood context. |
| `s2_l16_cell_id` | text | Immediate micro-context. |
| `created_at` | timestamptz |  |

### 5.3 `reverse_geocode_results`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `location_id` | uuid fk |  |
| `provider` | text | Google, Mappls, HERE, etc. |
| `provider_place_id` | text | Nullable. |
| `response_json` | jsonb | Terms-aware storage only. |
| `resolved_latitude` | numeric | If returned. |
| `resolved_longitude` | numeric | If returned. |
| `distance_from_selected_m` | numeric | Important for nearest-POI discipline. |
| `collected_at` | timestamptz |  |
| `cache_policy` | text |  |

### 5.4 `s2_cells`

Purpose:

- Store multi-resolution S2 cell records used for location character and S2Vec-inspired embeddings.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `cell_id` | text | Provider/library S2 cell token. |
| `level` | int | 12-16 for V1. |
| `parent_cell_id` | text | Nullable. |
| `geom` | geography(Polygon, 4326) | Cell boundary. |
| `center_geom` | geography(Point, 4326) | Cell centroid. |
| `created_at` | timestamptz |  |

### 5.5 `s2_cell_features`

Purpose:

- Store deterministic built-environment feature vectors aggregated per S2 cell.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `s2_cell_id` | uuid fk |  |
| `feature_version` | text | Versioned feature schema. |
| `feature_json` | jsonb | Counts, densities, ratios, public-web metrics. |
| `top_feature_labels` | text[] | Human-readable internal labels. |
| `source_run_refs` | uuid[] | Source runs contributing to this profile. |
| `coverage_note` | text | Missing/sparse data note. |
| `computed_at` | timestamptz |  |

### 5.6 `s2_cell_embeddings`

Purpose:

- Store S2Vec-inspired embeddings once the model-training pipeline exists.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `s2_cell_id` | uuid fk |  |
| `model_version` | text | Embedding model version. |
| `embedding` | vector | pgvector embedding. |
| `training_feature_version` | text | Feature set used for training. |
| `computed_at` | timestamptz |  |

### 5.7 `location_cell_profiles`

Purpose:

- Store report-specific profile labels for the selected pin's S2 cells.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `location_id` | uuid fk |  |
| `s2_cell_id` | uuid fk |  |
| `level` | int | 12-16. |
| `profile_labels` | text[] | e.g. office_residential_mixed. |
| `profile_summary` | text | Internal/explainable summary. |
| `source_planning_cues` | jsonb | Suggested source family priorities. |
| `preview_safe_summary` | text | Low-cost preview wording, no proof claims. |
| `data_limit_note` | text |  |
| `created_at` | timestamptz |  |

### 5.8 `similar_location_matches`

Purpose:

- Store similar S2 cells/locations for internal QA and future comparison products.

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `source_s2_cell_id` | uuid fk |  |
| `matched_s2_cell_id` | uuid fk |  |
| `model_version` | text |  |
| `similarity_score` | numeric | Internal only. |
| `match_reason_json` | jsonb | Explainable feature overlap. |
| `created_at` | timestamptz |  |

### 5.9 `previews`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `preview_json` | jsonb | Preview content. |
| `cost_class` | text | `low_cost`. |
| `created_at` | timestamptz |  |

### 5.10 `payments`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `provider` | text | Razorpay/Stripe/etc. |
| `checkout_session_id` | text |  |
| `payment_id` | text | Provider payment id. |
| `amount` | numeric |  |
| `currency` | text | INR. |
| `status` | text | Payment status enum. |
| `idempotency_key` | text |  |
| `provider_payload` | jsonb | Raw webhook payload. |
| `created_at` | timestamptz |  |
| `paid_at` | timestamptz |  |

### 5.11 `source_runs`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `source_id` | text | `google_places`, `playo`, etc. |
| `source_class` | text | commercial_api, public_web_gold, etc. |
| `status` | text | planned/running/succeeded/failed/skipped. |
| `started_at` | timestamptz |  |
| `finished_at` | timestamptz |  |
| `visible_locality` | text | For public-web gold. |
| `pin_conditioned` | boolean |  |
| `freshness_note` | text |  |
| `user_facing_source_note` | text |  |
| `internal_notes` | jsonb |  |

### 5.12 `raw_artifacts`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `source_run_id` | uuid fk |  |
| `artifact_type` | text | json/html/screenshot/image/pdf/map_render. |
| `storage_url` | text | Supabase Storage or S3 pointer. |
| `content_hash` | text |  |
| `terms_policy` | text | Storage/display rules. |
| `created_at` | timestamptz |  |

### 5.13 `normalized_observations`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `source_run_id` | uuid fk |  |
| `observation_type` | text | poi, price, route, platform_listing, official_signal. |
| `name` | text |  |
| `value_json` | jsonb | Normalized payload. |
| `geom` | geography(Geometry, 4326) | Nullable. |
| `radius_or_area` | text |  |
| `time_window` | text |  |
| `collected_at` | timestamptz |  |
| `data_limit_note` | text |  |

### 5.14 `pois`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `canonical_name` | text |  |
| `category` | text |  |
| `role` | text | demand_anchor, competitor, complement, etc. |
| `geom` | geography(Point, 4326) |  |
| `address_text` | text |  |
| `rating` | numeric | Nullable. |
| `review_count` | int | Nullable. |
| `created_at` | timestamptz |  |

### 5.15 `poi_source_links`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `poi_id` | uuid fk |  |
| `source_id` | text |  |
| `provider_place_id` | text |  |
| `source_url` | text |  |
| `source_payload` | jsonb | Terms-aware. |

### 5.16 `catchments`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `catchment_type` | text | distance_ring/travel_time. |
| `label` | text | 1km, 15_min_drive, etc. |
| `geom` | geography(Polygon, 4326) |  |
| `provider` | text |  |
| `data_limit_note` | text |  |

### 5.17 `travel_times`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `origin_label` | text |  |
| `destination_label` | text |  |
| `mode` | text | car, two_wheeler proxy, walk, transit. |
| `time_window` | text | weekday_evening, etc. |
| `duration_minutes` | numeric |  |
| `distance_km` | numeric |  |
| `provider` | text |  |
| `route_geom` | geography(LineString, 4326) | Nullable. |

### 5.18 `public_web_sessions`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `source_run_id` | uuid fk |  |
| `platform` | text | Zomato, Blinkit, Playo, etc. |
| `entry_url` | text |  |
| `visible_locality` | text |  |
| `location_set_method` | text | locality_search, coordinate, URL pattern. |
| `items_visible` | int | Nullable. |
| `session_metadata` | jsonb |  |
| `created_at` | timestamptz |  |

### 5.19 `pricing_records`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `source_run_id` | uuid fk |  |
| `platform` | text |  |
| `venue_name` | text |  |
| `sport_or_activity` | text |  |
| `observed_at` | timestamptz |  |
| `slot_start` | timestamptz | Nullable. |
| `slot_end` | timestamptz | Nullable. |
| `slot_duration_minutes` | int | Nullable. |
| `display_price` | numeric | Nullable. |
| `display_price_unit` | text | per_court, per_player, per_slot, not_clear. |
| `normalized_price_per_court_hour` | numeric | Nullable. |
| `normalization_status` | text | normalized, visible_but_not_normalized, not_comparable. |
| `normalization_note` | text |  |

### 5.20 `signals`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `aspect_panel` | text |  |
| `metric_type` | text |  |
| `label` | text |  |
| `value` | jsonb |  |
| `unit` | text |  |
| `radius_or_area` | text |  |
| `time_window` | text |  |
| `source_refs` | uuid[] | normalized observation/source ids. |
| `interpretation` | text |  |
| `data_limit_note` | text |  |
| `embedding` | vector | Optional. |

### 5.21 `visual_assets`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `visual_type` | text | exact_pin_map, catchment_map, pricing_chart, etc. |
| `title` | text |  |
| `caption` | text |  |
| `storage_url` | text |  |
| `provider` | text |  |
| `attribution` | text |  |
| `data_limit_note` | text |  |

### 5.22 `reports`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `public_token` | text unique | Same or linked token. |
| `schema_version` | text |  |
| `report_json` | jsonb | Must validate against output schema. |
| `html_storage_url` | text | Optional rendered HTML snapshot. |
| `pdf_storage_url` | text | Nullable until PDF ready. |
| `status` | text | completed/completed_with_data_gaps/failed. |
| `generated_at` | timestamptz |  |
| `emailed_at` | timestamptz |  |

### 5.23 `audit_events`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid pk |  |
| `report_request_id` | uuid fk |  |
| `event_type` | text |  |
| `message` | text |  |
| `metadata` | jsonb |  |
| `created_at` | timestamptz |  |

## 6. Row-Level Security

Customer-facing access:

- No Supabase client direct table access for public customers.
- API server reads/writes using service role.
- Public report access uses secure token checked by API.

Admin access:

- Separate admin auth.
- Admin RLS policies or server-side admin API only.

## 7. Indexes

Required indexes:

```sql
create index report_locations_geom_idx on report_locations using gist (geom);
create index pois_geom_idx on pois using gist (geom);
create index catchments_geom_idx on catchments using gist (geom);
create index report_requests_public_token_idx on report_requests (public_token);
create index report_requests_email_idx on report_requests (email);
create index source_runs_report_source_idx on source_runs (report_request_id, source_id, status);
create index pricing_records_report_platform_idx on pricing_records (report_request_id, platform, normalization_status);
create index signals_report_aspect_idx on signals (report_request_id, aspect_panel);
create index s2_cells_level_cell_idx on s2_cells (level, cell_id);
create index s2_cells_geom_idx on s2_cells using gist (geom);
create index location_cell_profiles_report_idx on location_cell_profiles (report_request_id, level);
create index similar_location_matches_report_idx on similar_location_matches (report_request_id, similarity_score);
```

Use pgvector ANN indexes for `s2_cell_embeddings.embedding` once embedding dimensionality and distance metric are fixed.

## 8. Email Events

Emails:

- Preview created: optional.
- Payment received: optional/payment-provider dependent.
- Report ready: required.
- Report failed/support: internal required.

Report-ready email must include:

- Report title.
- Location summary.
- Secure report link.
- Note that the report is generated from public/commercial/official sources and should be used for understanding, not final advice.

## 9. Admin API

Admin required before scale:

- Search report by email/report id.
- View payment status.
- View workflow status.
- View source runs.
- View S2 cell profile labels and feature summary.
- View similar-location matches when available.
- View raw artifacts where allowed.
- Retry failed report.
- Regenerate report from existing source data.
- Trigger refund/support flow.

## 10. API Acceptance Criteria

The API/data model is ready when:

- A no-login report request can be created.
- Exact pin can be resolved and confirmed.
- Preview can be stored and fetched.
- Payment webhook can idempotently start generation.
- Progress can be polled/streamed.
- Full report can be retrieved by secure token.
- Report JSON validates against schema.
- Supabase tables support exact-pin, source-run, public-web, pricing, visual, and report audit records.
- Supabase tables support S2 cell IDs, deterministic cell profiles, and future S2Vec-style embeddings.
- No V1 endpoint requires customer login.
