create extension if not exists postgis;
create extension if not exists vector;
create extension if not exists pgcrypto;

create table if not exists report_requests (
  id uuid primary key default gen_random_uuid(),
  public_token text unique not null default ('rt_' || encode(gen_random_bytes(32), 'hex')),
  email text not null,
  location_input text not null,
  use_case_input text not null,
  purpose_category text,
  sub_purpose text,
  selected_context jsonb not null default '{}'::jsonb,
  status text not null default 'created',
  payment_status text not null default 'not_started',
  current_stage text,
  progress_percent int not null default 0 check (progress_percent >= 0 and progress_percent <= 100),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists locations (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  selected_latitude numeric not null,
  selected_longitude numeric not null,
  geom geography(Point, 4326) not null,
  address_text text,
  locality text,
  city text,
  district text,
  state text,
  pin_code text,
  plus_code text,
  digipin text,
  geocode_quality_note text,
  pin_identity_state text not null default 'coordinate_confirmed',
  s2_l12_cell_id text,
  s2_l13_cell_id text,
  s2_l14_cell_id text,
  s2_l15_cell_id text,
  s2_l16_cell_id text,
  created_at timestamptz not null default now()
);

-- Some Supabase projects already have a generic public.locations table.
-- In that case, "create table if not exists" skips the LocationIQ shape, so
-- ensure the columns required by the API exist before indexes and inserts run.
alter table if exists locations
  add column if not exists report_request_id uuid references report_requests(id) on delete cascade,
  add column if not exists selected_latitude numeric,
  add column if not exists selected_longitude numeric,
  add column if not exists geom geography(Point, 4326),
  add column if not exists address_text text,
  add column if not exists locality text,
  add column if not exists city text,
  add column if not exists district text,
  add column if not exists state text,
  add column if not exists pin_code text,
  add column if not exists plus_code text,
  add column if not exists digipin text,
  add column if not exists geocode_quality_note text,
  add column if not exists pin_identity_state text default 'coordinate_confirmed',
  add column if not exists s2_l12_cell_id text,
  add column if not exists s2_l13_cell_id text,
  add column if not exists s2_l14_cell_id text,
  add column if not exists s2_l15_cell_id text,
  add column if not exists s2_l16_cell_id text,
  add column if not exists created_at timestamptz default now();

create table if not exists reverse_geocode_results (
  id uuid primary key default gen_random_uuid(),
  location_id uuid not null references locations(id) on delete cascade,
  provider text not null,
  provider_place_id text,
  response_json jsonb,
  resolved_latitude numeric,
  resolved_longitude numeric,
  distance_from_selected_m numeric,
  collected_at timestamptz not null default now(),
  cache_policy text
);

create table if not exists s2_cells (
  id uuid primary key default gen_random_uuid(),
  cell_id text not null,
  level int not null check (level between 0 and 30),
  parent_cell_id text,
  geom geography(Polygon, 4326),
  center_geom geography(Point, 4326),
  created_at timestamptz not null default now(),
  unique(level, cell_id)
);

create table if not exists s2_cell_features (
  id uuid primary key default gen_random_uuid(),
  s2_cell_id uuid not null references s2_cells(id) on delete cascade,
  feature_version text not null,
  feature_json jsonb not null default '{}'::jsonb,
  top_feature_labels text[] not null default '{}',
  source_run_refs uuid[] not null default '{}',
  coverage_note text,
  computed_at timestamptz not null default now()
);

create table if not exists s2_cell_embeddings (
  id uuid primary key default gen_random_uuid(),
  s2_cell_id uuid not null references s2_cells(id) on delete cascade,
  model_version text not null,
  embedding vector,
  training_feature_version text,
  computed_at timestamptz not null default now()
);

create table if not exists location_cell_profiles (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  location_id uuid references locations(id) on delete cascade,
  s2_cell_id uuid references s2_cells(id) on delete set null,
  level int not null check (level between 12 and 16),
  profile_labels text[] not null default '{}',
  profile_summary text,
  source_planning_cues jsonb not null default '{}'::jsonb,
  preview_safe_summary text,
  data_limit_note text,
  created_at timestamptz not null default now()
);

create table if not exists similar_location_matches (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  source_s2_cell_id uuid references s2_cells(id) on delete set null,
  matched_s2_cell_id uuid references s2_cells(id) on delete set null,
  model_version text,
  similarity_score numeric,
  match_reason_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists previews (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null unique references report_requests(id) on delete cascade,
  preview_json jsonb not null,
  cost_class text not null default 'low_cost',
  created_at timestamptz not null default now()
);

create table if not exists payments (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  provider text not null,
  checkout_session_id text unique,
  payment_id text,
  amount numeric,
  currency text not null default 'INR',
  status text not null default 'not_started',
  idempotency_key text,
  provider_payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  paid_at timestamptz
);

create table if not exists source_runs (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  source_id text not null,
  source_class text not null,
  status text not null default 'planned',
  started_at timestamptz,
  finished_at timestamptz,
  visible_locality text,
  pin_conditioned boolean,
  freshness_note text,
  user_facing_source_note text,
  internal_notes jsonb not null default '{}'::jsonb
);

create table if not exists raw_artifacts (
  id uuid primary key default gen_random_uuid(),
  source_run_id uuid not null references source_runs(id) on delete cascade,
  artifact_type text not null,
  storage_url text not null,
  content_hash text,
  terms_policy text,
  created_at timestamptz not null default now()
);

create table if not exists normalized_observations (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  source_run_id uuid references source_runs(id) on delete set null,
  observation_type text not null,
  name text,
  value_json jsonb not null default '{}'::jsonb,
  geom geography(Geometry, 4326),
  radius_or_area text,
  time_window text,
  collected_at timestamptz not null default now(),
  data_limit_note text
);

create table if not exists pois (
  id uuid primary key default gen_random_uuid(),
  canonical_name text not null,
  category text,
  role text,
  geom geography(Point, 4326),
  address_text text,
  rating numeric,
  review_count int,
  created_at timestamptz not null default now()
);

create table if not exists poi_source_links (
  id uuid primary key default gen_random_uuid(),
  poi_id uuid not null references pois(id) on delete cascade,
  source_id text not null,
  provider_place_id text,
  source_url text,
  source_payload jsonb
);

create table if not exists catchments (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  catchment_type text not null,
  label text not null,
  geom geography(Polygon, 4326),
  provider text,
  data_limit_note text
);

create table if not exists travel_times (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  origin_label text not null,
  destination_label text not null,
  mode text not null,
  time_window text,
  duration_minutes numeric,
  distance_km numeric,
  provider text,
  route_geom geography(LineString, 4326)
);

create table if not exists public_web_sessions (
  id uuid primary key default gen_random_uuid(),
  source_run_id uuid not null references source_runs(id) on delete cascade,
  platform text not null,
  entry_url text,
  visible_locality text,
  location_set_method text,
  items_visible int,
  session_metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists pricing_records (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  source_run_id uuid references source_runs(id) on delete set null,
  platform text not null,
  venue_name text,
  sport_or_activity text,
  observed_at timestamptz not null default now(),
  slot_start timestamptz,
  slot_end timestamptz,
  slot_duration_minutes int,
  display_price numeric,
  display_price_unit text,
  normalized_price_per_court_hour numeric,
  normalization_status text not null default 'visible_but_not_normalized',
  normalization_note text
);

create table if not exists signals (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  aspect_panel text not null,
  metric_type text,
  label text not null,
  value jsonb not null default '{}'::jsonb,
  unit text,
  radius_or_area text,
  time_window text,
  source_refs uuid[] not null default '{}',
  interpretation text,
  data_limit_note text,
  embedding vector
);

create table if not exists visual_assets (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  visual_type text not null,
  title text,
  caption text,
  storage_url text,
  provider text,
  attribution text,
  data_limit_note text
);

create table if not exists reports (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null unique references report_requests(id) on delete cascade,
  public_token text unique not null,
  schema_version text not null,
  report_json jsonb not null,
  html_storage_url text,
  pdf_storage_url text,
  status text not null default 'completed',
  generated_at timestamptz not null default now(),
  emailed_at timestamptz
);

create table if not exists audit_events (
  id uuid primary key default gen_random_uuid(),
  report_request_id uuid not null references report_requests(id) on delete cascade,
  event_type text not null,
  message text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists locations_geom_idx on locations using gist (geom);
create index if not exists pois_geom_idx on pois using gist (geom);
create index if not exists catchments_geom_idx on catchments using gist (geom);
create index if not exists report_requests_public_token_idx on report_requests (public_token);
create index if not exists report_requests_email_idx on report_requests (email);
create index if not exists source_runs_report_source_idx on source_runs (report_request_id, source_id, status);
create index if not exists pricing_records_report_platform_idx on pricing_records (report_request_id, platform, normalization_status);
create index if not exists signals_report_aspect_idx on signals (report_request_id, aspect_panel);
create index if not exists s2_cells_level_cell_idx on s2_cells (level, cell_id);
create index if not exists s2_cells_geom_idx on s2_cells using gist (geom);
create index if not exists location_cell_profiles_report_idx on location_cell_profiles (report_request_id, level);
create index if not exists similar_location_matches_report_idx on similar_location_matches (report_request_id, similarity_score);
