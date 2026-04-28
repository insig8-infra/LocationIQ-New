# India Signal Library

This file defines the signals LocationIQ should use for India-first location intelligence.

The goal is not to show every fact about a place. The goal is to interpret a location from the user's selected purpose and support each interpretation with useful numbers, source links, freshness context, and clearly worded limitations.

The user-facing report should not expose source-quality machinery as badges such as `direct`, `inferred`, `weak proxy`, or `certainty score`. Those can exist internally for QA, but the report should express source quality naturally in the wording.

## Signal Library Contract

Every signal should be represented as:

```yaml
signal:
  name: string
  aspect_panel: string
  metric_type: string
  value: number_or_string
  unit: string
  radius_or_area: string
  time_window: string
  source_type: string
  last_checked: string
  interpretation: string
  user_facing_source_note: string
  data_limit_note: string
  internal_data_quality: optional_object
  limitations: []
```

## Signal Families

| Signal family | What to measure | Why it matters | Typical metrics |
|---|---|---|---|
| Catchment strength | Residents, workers, students, visitors, household mix, apartment density, travel-time reach | Reveals who can realistically use or be affected by the location | population baseline, POI anchors, residential clusters, travel-time areas |
| POI ecosystem | Anchors, complements, substitutes, competitors, support services, friction sources | Turns nearby places into purpose-specific meaning | count by category, nearest distance, density, opening hours |
| Mobility and access | Roads, congestion, transit, walkability, last-200m access, parking, crossings, turns | Practical access often differs from map distance in Indian cities | distance, travel time, road class, transit count, route friction |
| Reviews and sentiment | Parking, crowding, safety, hygiene, waterlogging, noise, service, family/women/kids fit | Extracts local reputation from scattered public comments | review count, mention share, rating range, recency |
| Environmental comfort | AQI, noise, heat, dust, green cover, flood/waterlogging, monsoon vulnerability | Affects daily comfort, health, and operational reliability | AQI value, station distance, risk proximity, green/open-space count |
| Safety and after-dark comfort | Lighting, isolation, late-night activity, accident-prone stretches, gendered safety comments | Safety is highly time-dependent and micro-local | late-active POI count, safety mentions, accident/blackspot proximity |
| Civic reliability | Water, power, drainage, sewage, garbage, public toilets, road condition, telecom/internet | Decides real livability and business usability | complaint mentions, civic asset count, outage mentions |
| Local operating friction | Parking enforcement, loading limits, society restrictions, encroachment, hawker zones, signage friction | India-specific issues that maps often miss | field notes, review mentions, local complaints, route restrictions |
| Time-of-day behavior | Morning, lunch, evening, late-night, weekend, monsoon, festival | The same place can behave differently by hour or season | open POI count, traffic proxy, field count, review timestamp |
| Future change | Metro, roads, flyovers, RERA supply, offices, schools, hospitals, public works | Shows how the area may change or be disrupted | project count, distance, official date, construction proximity |
| Source quality and limits | Recency, source agreement, spatial precision, repeatability, missing data | Prevents false certainty without making the report feel like a proof dossier | source count, freshness note, spatial-resolution note, missing critical signals |

## Source Posture

LocationIQ should combine these source classes, not rely on only one:

- Official public sources
- Open-map and owned internal layers
- Commercial APIs and licensed datasets
- Public-web gold surfaces
- Imagery for human review or machine-usable street evidence
- Field observation and user-supplied evidence

Public-web gold means a public, user-visible, locality-conditioned platform surface that becomes meaningful only after the location is set. Examples include:

- Zomato locality delivery pages
- Swiggy restaurant discovery for a selected delivery area
- Blinkit and Zepto locality-conditioned catalogs
- Playo, Hudle, and KheloMore venue discovery surfaces

These surfaces should be collected only when:

- the selected pin can be mapped to the platform's visible locality or catchment,
- the captured surface clearly reflects that locality,
- the extracted fields are stable enough to be interpreted,
- and the report distinguishes visible platform supply from guaranteed transaction truth.

For user-facing language, prefer:

```text
Playo currently surfaces 80 Hinjawadi pickleball results. Treat this as platform visibility, not total market size.
```

Avoid:

```text
Evidence strength: Medium proxy.
```

## Catchment Signals

Measure:

- Resident population baseline
- Household and family profile where available
- Residential cluster count
- Apartment/township/project count
- Office and worker anchors
- Student anchors
- Tourist/visitor anchors
- Daytime vs nighttime population proxy
- 300 m, 1 km, 3 km, 5 km rings
- 10/15/30 min travel-time catchments by relevant mode

Quantified metrics:

```yaml
metrics:
  - resident_population_estimate
  - households_estimate
  - residential_cluster_count
  - office_anchor_count
  - education_anchor_count
  - healthcare_anchor_count
  - visitor_anchor_count
  - relevant_anchor_density_per_sq_km
  - travel_time_population_proxy
```

Interpretation examples:

```text
For a 3BHK home, nearby schools, healthcare, daily retail, and commute anchors matter more than raw population density.
```

```text
For pickleball, office and residential anchors within 3-5 km are more useful than random footfall because the activity is planned and repeat-driven.
```

Useful sources:

- Census of India Primary Census Abstract: https://censusindia.gov.in/nada/index.php/catalog/6191
- Census town/village/ward datasets: https://censusindia.gov.in/nada/index.php/catalog/study/PC11_PCA-TV-0505
- Open Government Data Platform India: https://www.data.gov.in/
- Bhuvan thematic layers: https://bhuvan.nrsc.gov.in/wiki/index.php/Thematic_Data
- PhonePe Pulse: https://www.phonepe.com/pulse/data-api/
- ONDC public data: https://ondc.org/
- Public-web gold locality surfaces where the purpose depends on local supply or convenience
- State RERA project portals where relevant
- Licensed POI/mobility data
- User/field observations

## POI Ecosystem Signals

Classify POIs by role:

| Role | Meaning |
|---|---|
| Demand anchor | Creates or concentrates relevant audience |
| Complement | Makes the purpose easier or more attractive |
| Direct competitor | Offers the same core use |
| Indirect substitute | Solves a similar need differently |
| Support service | Helps day-to-day usage |
| Friction source | Creates noise, traffic, safety, access, or perception issues |
| Neutral context | Nearby but not meaningfully relevant |

Quantified metrics:

```yaml
metrics:
  - poi_count_by_role_and_radius
  - nearest_anchor_distance
  - direct_competitor_count
  - indirect_substitute_count
  - complement_count
  - active_open_now_count
  - evening_active_poi_count
  - average_rating_by_category
  - review_volume_by_category
  - category_density_per_sq_km
```

Useful sources:

- Google Places, Mappls POI, HERE, and Foursquare Places where licensed
- Overture and OpenStreetMap for internal open-map context
- OpenStreetMap and Overpass API: https://wiki.openstreetmap.org/wiki/Overpass_API
- Licensed commercial POI providers
- Public-web gold surfaces such as Zomato, Swiggy, Blinkit, Zepto, Playo, Hudle, and KheloMore when the surface is locality-conditioned and purpose-relevant
- City/municipal asset datasets
- User-submitted field observations

Interpretation examples:

```text
For a cafe, offices and coaching centers may be demand anchors; gyms and salons may be complements; tea stalls and bakeries may be substitutes.
```

```text
For a home, bars or industrial units may be friction sources for families but less important for a young professional rental context.
```

## Marketplace, Booking, And Public-Web Gold Signals

Measure:

- Locality-conditioned listing count
- Category mix or cuisine mix
- Chain or branded presence
- Visible price-band distribution
- Displayed delivery ETA or fast-delivery promise
- Catalog assortment depth
- Availability posture
- Venue count by sport
- Booking-slot visibility and price cues
- Promoted or high-visibility listing concentration

Quantified metrics:

```yaml
metrics:
  - marketplace_listing_count
  - category_mix
  - visible_price_band_distribution
  - delivery_eta
  - catalog_assortment_count
  - availability_ratio
  - booking_venue_count
  - booking_slot_count
  - booking_price
  - promotional_visibility_count
```

Interpretation rules:

- Collect only from a surface that clearly reflects the selected pin's locality or catchment.
- Record the visible locality label, timestamp, and collection method.
- Treat listing visibility as a strong local demand, competition, or convenience proxy, not as guaranteed transaction truth.
- Use repeated collection or cross-platform comparison when ranking or personalization may bias the visible order.
- Do not let a national homepage or generic city page stand in for a locality-conditioned result.

Useful sources:

- Zomato locality delivery pages
- Swiggy restaurant discovery surfaces
- Blinkit locality-conditioned catalog
- Zepto locality-conditioned catalog
- Playo venue discovery
- Hudle venue discovery
- KheloMore venue discovery
- magicpin local discovery
- PhonePe Pulse for public merchant/payment context
- ONDC public ecosystem data for network maturity and discoverable supply context

Interpretation examples:

```text
For a cafe, a strong Zomato or Swiggy locality surface can show cuisine density, direct competitor visibility, rating pressure, and whether the area already behaves like an active food discovery pocket.
```

```text
For a dark store, Blinkit and Zepto locality catalogs can show whether the selected catchment already supports deep quick-commerce assortment, fast-delivery signaling, and strong category breadth.
```

```text
For pickleball or turf booking, Playo, Hudle, and KheloMore can reveal whether the nearby sports market is sparse, clustered, premium, price-led, coaching-led, or slot-constrained.
```

## Mobility And Last-Mile Signals

Measure:

- Road hierarchy
- Access from arterial road
- Last 200 m route quality
- Number of turns from main road
- Median/U-turn friction
- Public transport stops
- Metro/suburban rail access
- Walking comfort
- Footpath/crossing quality where available
- Parking and stopping space
- Cab/auto availability
- Delivery rider or freight access
- Peak-hour travel time
- Monsoon route vulnerability

Quantified metrics:

```yaml
metrics:
  - distance_to_arterial_road_m
  - nearest_bus_stop_distance_m
  - nearest_metro_station_distance_m
  - transit_stop_count_1km
  - estimated_travel_time_from_anchor_min
  - peak_delay_ratio
  - number_of_turns_from_main_road
  - parking_spaces_observed
  - two_wheeler_parking_spaces_observed
  - freight_turning_constraints_count
```

India-specific interpretation:

```text
Straight-line distance is not access. Flyovers, service roads, gates, U-turns, drains, informal parking, traffic police restrictions, and poor crossings can completely change practical usability.
```

Useful sources:

- OSM road graph and tags
- GTFS feeds where available, such as Delhi Open Transit Data: https://otd.delhi.gov.in/documentation
- GTFS reference: https://gtfs.org/
- Licensed traffic APIs
- IUDX/city data where available
- Field observations

## Reviews And Sentiment Signals

Extract patterns from nearby POIs and local public comments.

Themes to detect:

- Parking
- Traffic
- Waterlogging
- Safety
- Women/family/kids friendliness
- Hygiene and cleanliness
- Noise
- Crowd quality
- Road condition
- Delivery delay
- Lift/power/water issues
- Staff/service quality
- Price-positioning fit
- Difficult to find
- Slot scarcity or booking frustration where sports/public booking surfaces are relevant
- Delivery-time disappointment where public ordering platforms expose that signal

Quantified metrics:

```yaml
metrics:
  - review_count
  - recent_review_count_12_months
  - average_rating
  - rating_range
  - mention_count_by_theme
  - mention_share_by_theme
  - negative_theme_share
  - source_category_count
  - local_language_review_share
```

Interpretation rules:

- Repeated mentions across multiple POIs are stronger than one review.
- A high review count can indicate activity, but may be tourist-heavy or category-specific.
- Paid, manipulated, or suspicious review patterns should be called out as a limitation rather than treated as clean ground truth.
- Local-language reviews can surface ground truth that English reviews miss.

Example:

```text
Parking appears as 22 mentions across 180 sampled reviews in nearby restaurants and sports venues. For a family-oriented recreation facility, this is a meaningful arrival-friction signal, but field observation is still required.
```

Public-web gold review and listing surfaces can be especially useful here because they often combine rating depth, visible review volume, and category-specific complaints inside the same locality-conditioned experience.

## Environmental And Civic Signals

Measure:

- AQI
- Dust/construction exposure
- Noise corridors
- Heat and shade
- Green/open space
- Waterlogging/flood risk
- Drainage and sewage signals
- Garbage and waste issues
- Power reliability
- Water supply reliability
- Internet/mobile quality
- Road condition

Quantified metrics:

```yaml
metrics:
  - nearest_aqi_station_distance_km
  - aqi_value
  - green_space_count_1km
  - distance_to_major_road_m
  - flood_risk_layer_value
  - waterlogging_mentions_count
  - drainage_or_sewage_mentions_count
  - garbage_mentions_count
  - power_outage_mentions_count
  - telecom_quality_indicator
```

Useful sources:

- CPCB National Air Quality Index: https://cpcb.nic.in/national-air-quality-index/
- India Meteorological Department rainfall information: https://mausam.imd.gov.in/responsive/rainfallinformation.php
- Bhuvan thematic maps: https://bhuvan.nrsc.gov.in/wiki/index.php/Thematic_Data
- NRSC Flood Hazard Zonation Atlas: https://www.nrsc.gov.in/nrscnew/resources_atlas_FloodHazard_Zonation.php
- TRAI apps and telecom indicators where usable
- Civic complaint portals and city open data
- Field observations

Interpretation examples:

```text
For a home, AQI/noise/green cover are daily comfort signals.
```

```text
For outdoor sports, monsoon drainage and summer heat can shape actual usable hours.
```

## Safety And After-Dark Signals

Measure:

- Evening-active POIs
- Late-night transport support
- Street-lighting proxy
- Isolated road segments
- Accident-prone junctions
- Women-specific safety mentions
- Alcohol/nightlife crowd friction where relevant
- Police or security presence proxy

Quantified metrics:

```yaml
metrics:
  - evening_active_poi_count_500m
  - late_night_food_or_transport_count_1km
  - isolated_segment_count
  - safety_mentions_count
  - women_safety_mentions_count
  - accident_blackspot_distance_km
  - police_station_distance_km
```

Important caveat:

```text
Official crime data is usually too coarse for exact-pin interpretation. Treat it as background context, not precise micro-location truth.
```

## Local Operating Friction Signals

India-specific ground realities often decide real usability.

Watch for:

- Informal parking dependence
- Traffic police restrictions
- Hawker/encroachment pressure
- Society/RWA restrictions
- Loading/unloading limits
- Signage visibility issues
- Road digging and recurring public works
- Local resistance to noise/crowd
- Poor addressability
- Gate/security constraints

Quantified metrics:

```yaml
metrics:
  - observed_parking_spaces
  - restricted_or_informal_parking_count
  - loading_space_count
  - recurring_complaint_mentions
  - local_restriction_notes_count
  - access_gate_count
  - user_supplied_photo_count
```

Field sources are often necessary for these signals.

## Time-Based Behavior Signals

Measure by time window:

- Weekday morning
- Weekday lunch
- Weekday evening
- Late evening/night
- Weekend morning
- Weekend evening
- Monsoon/rain
- Festival/seasonal peak

Quantified metrics:

```yaml
metrics:
  - open_poi_count_by_time_window
  - traffic_time_by_window
  - field_footfall_count_15_min
  - parked_vehicle_count_15_min
  - competitor_occupancy_observed
  - review_timestamp_activity_proxy
```

Interpretation:

```text
Do not call a location active or dead without specifying time. A place can be strong for lunch, weak for dinner, safe by day, and uncomfortable after dark.
```

## Future Development Signals

Measure:

- Metro/transit projects
- Road widening/flyovers
- RERA residential pipeline
- Commercial/office supply
- New malls, hospitals, schools, campuses
- Industrial/logistics nodes
- Public works
- Construction disruption

Quantified metrics:

```yaml
metrics:
  - future_metro_station_distance_km
  - infrastructure_project_count_5km
  - rera_project_count_5km
  - construction_zone_count_1km
  - expected_completion_date
  - official_project_status
```

Interpretation:

```text
Future projects should be described as change signals. They are not guaranteed value creation. They can improve access later while increasing disruption now.
```

## Ground-Reality Watchout Catalogue

| Watchout | Quantified evidence | Observation prompt |
|---|---|---|
| Monsoon access | waterlogging mentions, flood layer proximity, low-lying segments | Visit after rain; ask about last three monsoons |
| Parking friction | observed spaces, parking mentions, road width, vehicle dependence | Count car/two-wheeler spaces at peak |
| Weak exact pin | low immediate POI count, low active frontage, field footfall count | Count passers and stoppers for 15 minutes |
| Safety after dark | late-active POI count, isolated segments, lighting notes | Visit after 9 PM with caution; observe transport and crowd |
| Demand illusion | high POI count but low occupancy/review recency | Observe actual occupancy and repeat-user behavior |
| Competition pressure | direct competitor count, rating/review volume, distance | Compare quality, pricing, availability, crowd, complaints |
| Civic reliability | water/power/garbage/drainage mentions | Ask residents, guards, shopkeepers, delivery riders |
| Construction disruption | construction zones, project timelines, road diversions | Check current barricades and official project timelines |
| Delivery/freight friction | route turns, parking/loading space, one-way delays | Observe rider/truck stopping and turnaround |
| Family discomfort | noise, bars, unsafe crossings, poor parks | Visit evening/weekend; check schools/parks/clinics |

## Signal Card Example

```yaml
id: signal_031
signal_name: "Evening sports audience"
aspect_panel: "target_audience_catchment"
metric_type: "poi_count"
numbers:
  - label: "office anchors"
    value: 8
    unit: "count"
    radius: "5km"
  - label: "large residential clusters"
    value: 11
    unit: "count"
    radius: "5km"
  - label: "sports/recreation facilities"
    value: 4
    unit: "count"
    radius: "3km"
interpretation: "The area shows a plausible after-work and weekend recreation audience."
user_facing_source_note: "This combines visible POI anchors and public listing data checked for the selected catchment."
data_limit_note: "POI counts do not measure actual booking intent."
limitations:
  - "POI counts do not measure actual booking intent."
ground_observation:
  - "Check occupancy at nearby sports facilities between 6 PM and 9 PM."
```

## Data Caveats

- Census data is official and fine-grained but old.
- POI data can be duplicated, stale, or incomplete.
- Review data can be biased, manipulated, or category-skewed.
- Traffic APIs may not capture the final 200 m.
- AQI/noise/flood data may be station-level or coarse.
- Official crime data is usually too coarse for exact pins.
- Field checks are part of the product, not a fallback.
