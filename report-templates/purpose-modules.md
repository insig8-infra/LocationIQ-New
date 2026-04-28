# Purpose Modules

Purpose modules define how the master interpretive report adapts to different user intents.

The module should not tell the user what to do. It should explain how to read the location through that purpose.

Each module defines:

- What the user is trying to understand
- Required context fields
- Highest-priority aspect panels
- Quantified evidence to collect
- POI roles
- Time windows
- Ground-reality watchouts
- On-ground observation plan
- Sub-purpose overrides

## Shared Purpose Module Contract

Every purpose module should produce these sections:

```yaml
purpose_module:
  purpose_category: string
  sub_purpose: string
  understanding_question: string
  required_context_fields: []
  primary_aspect_panels: []
  secondary_aspect_panels: []
  quantified_evidence_requirements: []
  preferred_public_web_gold_sources: []
  poi_role_mapping: {}
  time_windows_to_analyze: []
  ground_reality_watchouts: []
  observation_plan: []
```

## Shared Aspect Panels

Use these panels across purposes. The purpose module decides which panels are primary.

| Aspect panel | What it explains |
|---|---|
| Location orientation | What kind of place the exact pin is |
| Target audience catchment | Who naturally surrounds or reaches the pin |
| Daily/social infrastructure | Schools, hospitals, groceries, parks, banks, local support |
| Movement and access | How people arrive, commute, walk, park, load, or deliver |
| Time-based character | How the location changes by hour, day, season |
| Surrounding ecosystem | Anchors, complements, substitutes, competitors, friction sources |
| Competition and complementarity | What similar or supporting options exist nearby |
| Ground-reality watchouts | Civic, safety, weather, parking, noise, local friction |
| Environment and comfort | AQI, heat, noise, green cover, flooding, dust |
| Future change | Infrastructure, new supply, construction, area maturity |
| Exact-pin vs locality | Whether the specific pin is better/worse/different than the locality |
| Source-aware limitations | What is current, locality-level, stale, missing, or physically unverified |

## 1. Live Or Relocate

Purpose category: `live_relocate`

Sub-purposes:

- `rent_home`
- `buy_primary_home`
- `pg_or_coliving`
- `student_housing`
- `senior_living`
- `family_relocation`
- `second_home`

Understanding question:

```text
What would day-to-day life around this location feel like for this household profile?
```

Required context:

- Household type
- Work/school commute anchors
- Primary mobility mode
- Lifestyle preference
- Safety sensitivity
- Need for schools/healthcare/public transport

Primary aspect panels:

- Location orientation
- Daily/social infrastructure
- Movement and access
- Safety and after-dark comfort
- Civic reliability
- Environment and comfort
- Time-based character
- Future change

Quantified evidence to collect:

| Evidence | Minimum useful unit |
|---|---|
| Grocery/pharmacy/daily needs | Count within 500 m and 1 km |
| Schools/daycare | Count and nearest distance within 3 km |
| Hospitals/clinics/pharmacies | Count and nearest distance within 3/5 km |
| Parks/open spaces | Count and nearest distance within 1/3 km |
| Public transport | Stops/stations within 500 m/1 km/3 km |
| Commute | Estimated time to user anchors by selected mode |
| Daily convenience delivery surface | Visible food, grocery, pharmacy, and quick-commerce availability for the selected locality |
| Noise/AQI/heat/flood | Nearest station/layer value or risk proximity |
| Safety proxies | Late-evening active POIs, street-lighting proxy, isolated stretches |
| Civic reliability | Review/complaint mentions of water, power, garbage, drainage |
| Future change | Metro/road/project count and distance |

POI role mapping:

```yaml
demand_or_lifestyle_anchors:
  - schools
  - hospitals
  - offices
  - parks
  - markets
  - transit stations
complements:
  - grocery
  - pharmacy
  - clinic
  - bank
  - daycare
  - restaurant
  - fitness
friction_sources:
  - highways
  - industrial units
  - bars/nightlife for family contexts
  - dump yards
  - drains
  - noisy roads
  - construction zones
```

Interpretation guidance:

- Explain lifestyle fit, not resale or investment return.
- Distinguish exact building/pin from broader locality reputation.
- Show commute reality by time window, not only distance.
- Highlight whether daily needs are walkable or vehicle-dependent.
- Use public-web delivery and quick-commerce surfaces as day-to-day convenience signals where the selected locality is clearly supported.
- Treat civic and environmental signals as major report value.

Sub-purpose overrides:

`buy_primary_home`

- Emphasize long-term livability, civic reliability, schools/healthcare, future change, and area maturity.
- Include "what may change in 3-5 years" but avoid price/appreciation advice.
- Quantify nearby residential supply only as future crowd/infrastructure context.

`rent_home`

- Emphasize commute, daily convenience, safety, noise, and transport.
- Reduce future-change weight unless it affects near-term construction or commute.

`pg_or_coliving` and `student_housing`

- Emphasize colleges/coaching/office access, late-evening food, transit, safety, laundry/medical, affordability proxy only as area positioning.
- Include late-night and weekend character.

`senior_living`

- Emphasize hospitals, pharmacies, walkability, lift/road comfort, noise, traffic stress, parks, and emergency access.

Observation plan:

- Visit on weekday morning and evening commute windows.
- Walk to grocery, pharmacy, transit, and park if relevant.
- Check street lighting after 9 PM.
- Ask residents/guards about water, power, garbage, flooding, noise, and mosquitoes.
- Visit after rain if the area has monsoon risk.

## 2. Retail, Food, Or Local Service Business

Purpose category: `retail_fnb_site`

Sub-purposes:

- `cafe`
- `quick_service_restaurant`
- `restaurant`
- `cloud_kitchen`
- `grocery_or_kirana`
- `pharmacy`
- `salon_or_spa`
- `fashion_or_electronics_store`
- `franchise_store`
- `street_kiosk`
- `pet_store`
- `bakery_or_dessert`

Understanding question:

```text
What kind of customer movement, nearby ecosystem, and operating reality does this location show for this business format?
```

Required context:

- Business format
- Target customer
- Positioning
- Daypart priority
- Frontage need
- Parking need
- Delivery/walk-in/dine-in dependence

Primary aspect panels:

- Exact-pin visibility
- Target audience catchment
- Movement and access
- Demand anchors
- Competition and complementarity
- Time-based character
- Parking and arrival
- Ground-reality watchouts

Quantified evidence to collect:

| Evidence | Minimum useful unit |
|---|---|
| Direct competitors | Count within 300 m, 1 km, 3 km |
| Indirect substitutes | Count by category within 1 km |
| Complements | Count of offices/schools/gyms/salons/coworking etc. |
| Review volume | Reviews and rating range for nearby competitors |
| Opening-hour overlap | Number of relevant POIs open in target daypart |
| Transit/footfall proxies | Stops, offices, schools, markets, active frontages |
| Parking/arrival | Field or map-observed spaces, road width, stopping ease |
| Delivery ecosystem | Delivery-friendly residential catchment and rider access |
| Public-web food discovery surface | Zomato/Swiggy listing count, cuisine mix, rating depth, promoted density, delivery-time posture for the selected locality |
| Public-web quick-commerce surface | Blinkit/Zepto assortment depth, category breadth, visible availability, delivery promise where relevant |
| Waterlogging/construction | Watchout count and proximity |

POI role mapping:

```yaml
demand_anchors:
  - offices
  - colleges
  - coaching_centers
  - schools
  - hospitals
  - residential_societies
  - transit_nodes
  - markets
direct_competitors:
  cafe:
    - cafes
    - coffee_shops
    - bakeries
  quick_service_restaurant:
    - qsr
    - fast_food
    - takeaway
  pharmacy:
    - pharmacies
    - chemists
  salon_or_spa:
    - salons
    - spas
    - beauty_parlours
indirect_substitutes:
  - tea_stalls
  - street_food
  - tiffin_centers
  - convenience_stores
  - cloud_kitchens
complements:
  - gyms
  - coworking
  - offices
  - clinics
  - schools
  - bookstores
  - hostels
  - residential_clusters
```

Interpretation guidance:

- Do not say "this business will work". Explain the customer-flow and ecosystem signals.
- Separate walk-in demand from destination demand and delivery demand.
- Explain if competition validates category awareness or suggests saturation.
- Show whether the exact pin has visibility or only the wider locality has demand.
- When locality-conditioned public-web surfaces exist, use them as live neighborhood demand and competition evidence, but distinguish visible platform presence from proven transaction volume.

Sub-purpose overrides:

`cafe`

- Quantify student/office/residential anchors, food and beverage competitors, evening-active POIs, parking, and dwell-time complements.
- Interpret whether the area supports hangout, work-friendly, quick coffee, or delivery-led cafe behavior.

`cloud_kitchen`

- De-emphasize frontage and walkability.
- Emphasize delivery radius, residential density, rider access, addressability, traffic, late-evening order ecosystem, and Zomato/Swiggy locality-conditioned supply surfaces.

`restaurant`

- Emphasize family arrival, car parking, evening safety, destination ability, and complementary entertainment.

`pharmacy`

- Emphasize residential density, clinics/hospitals, senior population proxies, 24x7 access, emergency arrival, and quick-commerce or delivery availability where the public locality surface is strong.

`grocery_or_kirana`

- Emphasize residential density, repeat purchase convenience, rider access, Blinkit/Zepto category breadth, and whether the locality already behaves like a fast-delivery catchment.

`franchise_store`

- Emphasize brand-audience fit, visibility, category adjacency, observable competitor attributes, and mall/high-street/market suitability.

Observation plan:

- Visit during target business peak and weak time windows.
- Count passers, stoppers, parked vehicles, and competitor occupancy for 15 minutes.
- Photograph frontage, signage visibility, parking, road edge, and pedestrian access.
- Ask nearby shopkeepers about peak hours, waterlogging, enforcement, and customer profile.
- Observe delivery rider activity if delivery matters.

## 3. Fitness, Sports, Or Recreation

Purpose category: `fitness_sports`

Sub-purposes:

- `gym`
- `yoga_or_pilates_studio`
- `dance_studio`
- `sports_academy`
- `turf_or_court_booking`
- `pickleball_facility`
- `swimming_or_indoor_sports`
- `kids_activity_center`
- `martial_arts`

Understanding question:

```text
What repeat sports/recreation audience, access pattern, facility context, and time-window behavior does this location show?
```

Required context:

- Target audience
- Age group
- Primary mobility mode
- Time windows
- Parking need
- Indoor/outdoor/covered format
- Coaching vs booking vs membership model

Primary aspect panels:

- Target audience catchment
- Movement and arrival
- Parking and after-dark safety
- Competition and sports ecosystem
- Time-based character
- Weather-day user experience
- Arrival and user experience
- Community and repeat-usage signals

Quantified evidence to collect:

| Evidence | Minimum useful unit |
|---|---|
| Residential clusters | Count within 1/3/5 km |
| Office anchors | Count within 3/5 km |
| Schools/colleges | Count within 3 km for youth sports |
| Sports competitors | Count by sport within 1/3/5 km |
| Complementary fitness POIs | Gyms, studios, sports shops, cafes, physiotherapy |
| Evening-active support POIs | Food, cafes, transport, lit commercial activity |
| Travel time | From office/residential anchors during 6-9 PM |
| Parking | Observed availability during peak, user-supplied count, or clearly listed parking cue |
| Review themes | Mentions of parking, surface, lighting, washrooms, crowding, with sample size where available |
| Public booking ecosystem | Playo/Hudle/KheloMore venue count, sport mix, slot visibility, slot duration, and price unit within the selected catchment |
| Weather-day experience | Outdoor/indoor/covered format for nearby operators and field prompts for rain-day arrival |

POI role mapping:

```yaml
demand_anchors:
  - residential_societies
  - it_parks
  - offices
  - schools
  - colleges
  - townships
  - hostels
direct_competitors:
  - pickleball_courts
  - turfs
  - badminton_courts
  - tennis_courts
  - gyms
  - sports_academies
indirect_substitutes:
  - clubs
  - society_sports_areas
  - public_playgrounds
  - fitness_studios
complements:
  - cafes
  - juice_bars
  - physiotherapy
  - sports_retail
  - parking_lots
  - corporate_offices
```

Interpretation guidance:

- Explain whether this is a planned-visit location or walk-in friendly location.
- For sports, repeat usage matters more than one-time footfall.
- Existing sports facilities can validate the area as a recreation cluster.
- Competition increases differentiation pressure: court quality, lighting, covered play, coaching, community, washrooms, parking.
- Evening and weekend access should be analyzed separately.
- Public booking/discovery surfaces are especially valuable here because they show how the sports category is already organized for users in that catchment.
- Treat listing presence and slot visibility as strong competitor and behavior evidence, but not as guaranteed repeat revenue.
- Do not let one nearby sports anchor carry the demand story. Use exact-pin context, adjacent operators, same-category competitors, residential/office anchors, convenience surfaces, and arrival data together.
- Do not claim court-fit, drainage, lighting feasibility, legal suitability, or parking capacity for the exact plot unless reliable measured or field data exists.

Sub-purpose overrides:

`pickleball_facility`

- Quantify nearby pickleball courts and adjacent sports facilities within 3/5 km.
- Count office and residential anchors separately.
- Include beginner/coaching/community cues only when visible through booking pages, operator pages, review themes, photos, or field evidence.
- Analyze indoor, outdoor, and covered formats for nearby competitors; do not infer weather readiness for the selected plot from remote data alone.
- Look for evening-active support ecosystem, corporate booking potential, and public booking-platform competitor visibility on Playo, Hudle, and KheloMore.
- Normalize pricing from slot-level scrapes before comparing venues: duration, court/player unit, weekday/weekend, peak/non-peak, and add-ons.

`gym`

- Emphasize dense residential catchment, young-professional audience, morning/evening access, observable competitor differences, parking, and after-dark comfort.

`sports_academy`

- Emphasize school/family catchment, parent pickup/drop, weekend behavior, child safety, and waiting areas.

`turf_or_court_booking`

- Emphasize group arrival, evening lighting, parking, washrooms/changing rooms, booking slots, monsoon use, and public booking-platform visibility.

Observation plan:

- Visit 6-9 AM, 6-9 PM, and weekend morning/evening.
- Count active users at nearby sports facilities only as field observation, not as a remote-data assumption.
- Check parking and lighting after sunset.
- Ask players what they dislike about current facilities.
- Check washrooms, changing, water, seating, and rain recovery.
- Test travel time from two major office clusters and two residential clusters.

## 4. Education, Coaching, Or Childcare

Purpose category: `education_childcare`

Sub-purposes:

- `preschool`
- `school`
- `coaching_center`
- `skill_training_center`
- `tuition_center`
- `daycare`
- `student_hostel_or_pg`

Understanding question:

```text
What student/parent catchment, access safety, trust signals, and daily operating context does this location show?
```

Required context:

- Age group
- Student/parent target
- Commute mode
- Safety priority
- Operating hours
- Pickup/drop need

Primary aspect panels:

- Student/parent catchment
- Safety and access
- Pickup/drop and parking
- Surrounding education ecosystem
- Competition and complementarity
- Time-based character
- Civic and environment comfort

Quantified evidence to collect:

| Evidence | Minimum useful unit |
|---|---|
| Schools/colleges/coaching | Count and nearest distance within 1/3/5 km |
| Residential family clusters | Count within 3 km |
| Transit stops | Count within 500 m/1 km |
| Road safety | Major crossings, arterial proximity, accident/traffic proxy |
| Pickup/drop feasibility | Road width, stopping areas, parking observations |
| Complementary POIs | Stationery, food, libraries, hostels, print shops |
| Competitor review quality | Ratings, reviews, complaints |
| Noise/pollution | Road noise/AQI/dust exposure |

POI role mapping:

```yaml
demand_anchors:
  - residential_societies
  - schools
  - colleges
  - hostels
  - coaching_clusters
complements:
  - stationery
  - libraries
  - print_shops
  - food
  - public_transport
  - parks
friction_sources:
  - high_speed_roads
  - bars
  - isolated_lanes
  - construction_sites
  - noisy_industrial_edges
```

Interpretation guidance:

- For children, arrival safety can matter more than catchment size.
- For coaching, clustering can be positive because students already travel there.
- For daycare/preschool, trust, safety, cleanliness, and parent convenience dominate.

Sub-purpose overrides:

`preschool` and `daycare`

- Emphasize child-safe entry, parent parking, low traffic stress, cleanliness, nearby family clusters.

`coaching_center`

- Emphasize public transport, evening safety, student food/stationery ecosystem, cluster effect, and competitor density.

`student_hostel_or_pg`

- Emphasize late-evening food, transit, laundry, medical access, safety, and commute to education anchors.

Observation plan:

- Visit during school opening/closing or class change times.
- Observe pickup/drop congestion and crossing safety.
- Ask stationery/food shops about student movement.
- Check lighting and active frontage after evening classes.

## 5. Healthcare Or Wellness

Purpose category: `healthcare_wellness`

Sub-purposes:

- `clinic`
- `diagnostic_center`
- `pharmacy`
- `dental_or_eye_clinic`
- `physiotherapy`
- `elder_care`
- `hospital_access_for_living`

Understanding question:

```text
What patient/caregiver access, healthcare ecosystem, trust context, and repeat-visit practicality does this location show?
```

Required context:

- Patient profile
- Specialty
- Accessibility need
- Operating hours
- Emergency need
- Elderly/disabled access need

Primary aspect panels:

- Patient catchment
- Access and arrival
- Healthcare ecosystem
- Ground-floor/lift/parking fit
- Trust and review signals
- Safety and civic reliability
- Time-based character

Quantified evidence to collect:

| Evidence | Minimum useful unit |
|---|---|
| Residential catchment | Count/clusters within 3/5 km |
| Hospitals/clinics/pharmacies | Count and nearest distance |
| Diagnostic/therapy competitors | Count within 1/3/5 km |
| Accessibility | Distance from parking/transit, lift/ground-floor data if supplied |
| Review signals | Review count, rating range, complaints around wait, parking, access |
| Emergency access | Travel time to hospitals, road congestion, ambulance stopping ease |
| Elderly comfort | Walkability, shade, crossing safety, seating/waiting support |

POI role mapping:

```yaml
demand_anchors:
  - residential_clusters
  - senior_living
  - offices
  - hospitals
  - clinics
complements:
  - pharmacies
  - diagnostics
  - physiotherapy
  - medical_stores
  - labs
  - cafes_waiting
direct_competitors:
  - same_specialty_clinics
  - diagnostic_centers
  - pharmacies
friction_sources:
  - stairs_no_lift
  - no_parking
  - heavy_traffic
  - poor_ambulance_access
```

Interpretation guidance:

- Healthcare location value depends heavily on practical arrival.
- Patient and caregiver comfort should be interpreted separately.
- Clustered healthcare can be positive for trust and referrals.
- Exact floor/building access can change the location story.

Observation plan:

- Visit during morning and evening patient peaks.
- Check cab/auto stopping, lift/stairs, waiting spillover, and parking.
- Ask nearby pharmacies about patient flow and common specialties.
- Observe elderly/wheelchair access from parking or transit.

## 6. Office Or Workspace

Purpose category: `office_workspace`

Sub-purposes:

- `startup_office`
- `corporate_office`
- `coworking`
- `sales_branch`
- `back_office_or_bpo`
- `professional_services_office`

Understanding question:

```text
What employee, client, vendor, and daily operating context does this location create?
```

Required context:

- Team profile
- Employee commute mode
- Client visit frequency
- Operating hours
- Parking need
- Late-shift need
- Internet/power sensitivity

Primary aspect panels:

- Employee commute catchment
- Client/vendor access
- Daily support ecosystem
- Civic reliability
- Safety after dark
- Parking and building access
- Professional cluster/reputation
- Future change

Quantified evidence to collect:

| Evidence | Minimum useful unit |
|---|---|
| Transit access | Stops/stations within 500 m/1 km/3 km |
| Employee anchors | Residential clusters or talent hubs within 5/10 km |
| Food/daily support | Count of lunch, bank, courier, print, hotel POIs |
| Competing offices/coworking | Count and review quality |
| Parking | Field or building supplied capacity |
| Internet/power signals | Complaints, provider availability, power-cut mentions |
| Safety | Evening active POIs, lighting proxy, late-shift transport |

POI role mapping:

```yaml
demand_or_ecosystem_anchors:
  - offices
  - coworking
  - business_parks
  - transit
  - hotels
  - restaurants
complements:
  - banks
  - couriers
  - print_shops
  - cafes
  - stationery
  - gyms
friction_sources:
  - poor_parking
  - low_late_night_activity
  - unreliable_power
  - weak_public_transport
```

Interpretation guidance:

- Explain the office day: arrival, lunch, client visits, late exits, vendor movement.
- For coworking, surrounding cafes and startup ecosystem matter.
- For BPO/back office, late-shift safety and transport matter more.

Observation plan:

- Test employee commute routes at start/end times.
- Check lunch options and daily services within 500 m.
- Observe cab pickup/drop and parking.
- Ask current building occupants about power, internet, water, and security.

## 7. Logistics, Warehouse, Or Industrial

Purpose category: `logistics_industrial`

Sub-purposes:

- `warehouse`
- `dark_store`
- `last_mile_hub`
- `manufacturing_unit`
- `cold_chain`
- `fleet_parking`
- `mandi_or_procurement_point`

Understanding question:

```text
What goods movement, vehicle access, labor, utility, and operating-friction context does this location show?
```

Required context:

- Vehicle type
- Service radius
- Operating hours
- Loading need
- Power/utility need
- Labor need
- Inventory type

Primary aspect panels:

- Freight access
- Last-mile/service radius
- Loading and parking fit
- Utility reliability
- Labor and support ecosystem
- Environmental/monsoon risk
- Local operating friction
- Future road/infrastructure change

Quantified evidence to collect:

| Evidence | Minimum useful unit |
|---|---|
| Highway/arterial access | Distance and travel time |
| Road class/width | OSM/map/field classification |
| Turns/height restrictions | Count and description |
| Industrial/logistics POIs | Count within 3/5/10 km |
| Residential delivery catchment | Population/residential clusters within SLA radius |
| Quick-commerce locality surface | Blinkit/Zepto category breadth, assortment depth, and visible delivery-speed posture where the selected locality is covered |
| Labor/support | Nearby settlements, food, repair, fuel, mechanic POIs |
| Flood/heat risk | Risk layer/proximity |
| Accident/blackspot | Official/proxy signal where available |

POI role mapping:

```yaml
operations_anchors:
  - highways
  - arterial_roads
  - industrial_areas
  - logistics_parks
  - fuel_stations
  - repair_shops
  - labor_settlements
complements:
  - vehicle_service
  - food_for_workers
  - weighing_bridges
  - packaging_suppliers
friction_sources:
  - narrow_roads
  - residential_gates
  - traffic_restrictions
  - low_bridges
  - flood_prone_segments
```

Interpretation guidance:

- Map distance is much less important than vehicle approach.
- Analyze by vehicle type: two-wheeler, LCV, truck, container.
- For dark stores, dense demand catchment and rider access matter more than highway access.
- For dark stores and last-mile hubs, locality-conditioned quick-commerce surfaces are useful demand and competitive context because they reveal how the catchment already behaves online.
- For cold chain, power reliability and backup feasibility are critical watchouts.

Observation plan:

- Drive the route with the largest expected vehicle type.
- Check turning radius, road width, loading area, night access, and parking.
- Ask nearby operators about police restrictions, flooding, power cuts, and traffic windows.
- Time the route during expected dispatch windows.

## 8. Travel, Leisure, Or Short Stay

Purpose category: `travel_leisure`

Sub-purposes:

- `hotel_or_homestay`
- `tourist_day_plan`
- `family_outing`
- `nightlife_or_dining`
- `religious_visit`
- `workation`
- `event_trip`

Understanding question:

```text
What convenience, safety, comfort, and experience context does this location create for the trip purpose?
```

Required context:

- Traveler type
- Travel mode
- Time context
- Group size
- Duration
- Safety sensitivity
- Interest tags

Primary aspect panels:

- Attraction and itinerary access
- Safety and after-dark comfort
- Food/daily support
- Mobility and parking
- Crowd/seasonality
- Cleanliness and civic comfort
- Noise and rest quality
- Time-based character

Quantified evidence to collect:

| Evidence | Minimum useful unit |
|---|---|
| Attractions | Count and distance/time |
| Food/cafes | Count within 500 m/1 km |
| Transport | Station/airport/bus/metro distance and travel time |
| Hotels/stays | Count, rating range, review volume |
| Safety support | Late-night active POIs, police/transport proximity |
| Cleanliness/civic | Review mentions of toilets, garbage, crowding |
| Public discovery surface | Dining, nightlife, or attraction discovery density and visible review depth on purpose-relevant public platforms |
| Seasonality | Festival/crowd events, weather window, closure timings |

POI role mapping:

```yaml
experience_anchors:
  - attractions
  - religious_places
  - beaches
  - forts
  - museums
  - restaurants
  - nightlife
  - event_venues
complements:
  - hotels
  - cafes
  - toilets
  - parking
  - medical
  - atm
  - transport
friction_sources:
  - unsafe_late_night_stretches
  - overcrowding
  - poor_cleanliness
  - parking_shortage
  - noise
```

Interpretation guidance:

- Explain experience quality by traveler type.
- For families/seniors, toilets, shade, parking, and medical access matter.
- For nightlife, late-night transport and safety dominate.
- For workation, internet, power, noise, and cafe/work ecosystem matter.
- Public dining and venue-discovery surfaces can help show whether the area is actively used and discoverable by travelers at the relevant time of day.

Observation plan:

- Check arrival and departure during likely trip time.
- Observe crowding, cleanliness, parking, and cab/auto access.
- For night use, verify lighting and transport after dark.
- For seasonal places, compare normal vs peak-season behavior.

## Purpose Module Output Example

```yaml
purpose_interpretation:
  purpose_category: "fitness_sports"
  sub_purpose: "pickleball_facility"
  location_character: "emerging sports cluster near office-residential catchment"
  primary_aspects:
    - target_audience_catchment
    - movement_and_arrival
    - competition_complementarity
    - time_based_character
    - weather_resilience
  key_quantified_evidence:
    - "direct sports competitors within 3 km"
    - "office anchors within 5 km"
    - "residential clusters within 5 km"
    - "weekday evening travel time from key anchors"
    - "parking spaces observed during peak slot"
  interpretation_style: "Explain support/friction/unknowns; do not advise whether to invest."
```
