create extension if not exists postgis;

create table if not exists report_locations (
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

alter table if exists reverse_geocode_results
  drop constraint if exists reverse_geocode_results_location_id_fkey,
  drop constraint if exists reverse_geocode_results_report_location_id_fkey;

do $$
begin
  if to_regclass('public.reverse_geocode_results') is not null
    and not exists (
      select 1
      from pg_constraint
      where conname = 'reverse_geocode_results_report_location_id_fkey'
    )
  then
    alter table public.reverse_geocode_results
      add constraint reverse_geocode_results_report_location_id_fkey
      foreign key (location_id) references public.report_locations(id) on delete cascade;
  end if;
end $$;

alter table if exists location_cell_profiles
  drop constraint if exists location_cell_profiles_location_id_fkey,
  drop constraint if exists location_cell_profiles_report_location_id_fkey;

do $$
begin
  if to_regclass('public.location_cell_profiles') is not null
    and not exists (
      select 1
      from pg_constraint
      where conname = 'location_cell_profiles_report_location_id_fkey'
    )
  then
    alter table public.location_cell_profiles
      add constraint location_cell_profiles_report_location_id_fkey
      foreign key (location_id) references public.report_locations(id) on delete cascade;
  end if;
end $$;

create index if not exists report_locations_geom_idx on report_locations using gist (geom);
