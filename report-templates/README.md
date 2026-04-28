# LocationIQ Report Templates

This directory defines the report foundation for LocationIQ.

The product should not tell a user whether to buy, invest, open, or avoid. It should help the user understand and visualize a location from many angles so they can make their own decision with better context.

Core product promise:

```text
We do not decide for the user. We help the user see the location clearly.
```

## Product Direction

The app receives:

```text
location + purpose + sub-purpose + selected context
```

The app returns:

```text
a purpose-aware location intelligence report with rich interpretation, quantified evidence, source-aware limitations, unknowns, and on-ground observation prompts
```

The app should answer:

```text
What is this location like for this purpose?
What does it naturally support?
What creates friction?
What is visible in the evidence?
What is uncertain?
What should the user observe physically?
How does the exact pin differ from the broader locality?
```

It should avoid:

- Final investment advice
- Buy/sell/open/avoid recommendations
- A single overall score that pretends to decide the outcome
- Generic locality summaries
- Unsupported certainty
- Legal, financial, or compliance-heavy conclusions
- Parcel, safety, cleanliness, crowd-type, or physical-suitability claims that the data cannot reliably support

## Architecture

Use a shared interpretive report spine with purpose-specific modules.

Do not create completely separate report products for cafe, gym, home, warehouse, clinic, school, travel, and so on. Most location decisions share the same analytical grammar:

- Location orientation
- Purpose lens
- Catchment
- Surrounding ecosystem
- Movement and access
- Time-based behavior
- Audience/demand signals
- Competition and complementarity
- Ground-reality friction
- Future change
- Quantified evidence
- Source-aware limitations
- On-ground observation plan

Purpose modules should change:

- The context fields asked from the user
- The aspect panels shown more prominently
- The catchment radii and travel-time views
- The metrics used as evidence
- The interpretation rules
- The POI categories considered competitors, complements, anchors, or friction
- The field observations recommended to the user

## Locked Source Posture

These templates now assume a five-layer source posture:

1. Official and public baseline sources for India context, environment, hydrology, planning, and telecom benchmarks.
2. Open-map and owned-data layers for internal joins, reconciliation, and catchment analytics.
3. Commercial APIs and licensed datasets where they materially improve exact-pin quality, POI quality, routing, imagery, or change detection.
4. Public-web gold surfaces when a user-facing platform exposes a strong, location-conditioned page after the locality, delivery area, city, or venue radius is selected.
5. Field observation and user-supplied evidence to resolve what no dataset can settle cleanly.

Public-web gold is a first-class source class in this system.

That means:

- If a public platform shows a strong locality-conditioned surface, the product should collect it.
- The collection must be pin-conditioned, not blind.
- Partnership data can enrich the same source family, but partnership is not required to justify using it.
- Hidden, auth-only, or brittle private surfaces should not become foundational dependencies.
- Google Street View remains human-review/display evidence, while machine-usable street evidence should come from sources explicitly usable for that workflow.

## Files

- `input-taxonomy.yaml`
  Predefined purpose categories, sub-purposes, context fields, audiences, mobility modes, time contexts, and signal dimensions.

- `master-report-template.md`
  Canonical interpretive report structure. This replaces the old verdict-style report with a visual, evidence-backed location understanding format.

- `reader-first-v2-blueprint.md`
  Historical V2 blueprint retained for comparison only. Do not use it as the production basis for the technical spec.

- `reader-first-v4-blueprint.md`
  Current reader-first direction for production-grade reports. It keeps sources woven into the narrative instead of turning the report into a proof dossier, separates exact-pin truth from nearest-POI snapping, requires multi-anchor demand interpretation, upgrades visual standards, removes unsupported physical-suitability claims, and defines India-realistic data rules.

- `purpose-modules.md`
  Purpose-specific report playbooks for living, retail/F&B, fitness/sports, education, healthcare, office, logistics, and travel/leisure use cases.

- `scoring-and-confidence.md`
  Aspect-signal rules, quantified evidence rules, source-quality handling, and language guidelines. The historical filename is retained for continuity, but the current direction avoids user-facing certainty badges and final overall verdicts.

- `india-signal-library.md`
  India-first signal library: catchment, POI, mobility, reviews, civic, environmental, safety, local friction, time-of-day, and future development signals.

- `output-schema.json`
  Structured output schema for an interpretive, evidence-backed report.

## Report Philosophy

Each report should feel like a layered mental map.

The user should be able to understand:

- What the place is
- Who surrounds it
- How people reach it
- What happens at different times
- What nearby places help or hurt the purpose
- What the area feels like operationally
- What numbers support the interpretation
- What is missing or uncertain
- What to verify by visiting

## Quantified Evidence Principle

Interpretation is useful only when it is tied to evidence.

Wherever possible, every important claim should include numbers:

- Count of relevant POIs within 300 m, 1 km, 3 km, 5 km
- Distance to nearest anchors
- Travel time by mode
- Number of competitors and complements
- Review count, rating range, review recency
- Share of reviews mentioning parking, crowding, safety, waterlogging, cleanliness, etc.
- Count of transit stops or metro stations within reach
- Distance to arterial roads
- Number of schools/hospitals/offices/residential clusters nearby
- AQI, flood, heat, noise, or civic signal values when available
- Construction or future-development items within a defined radius

When numbers are not available, the report should say so and phrase the interpretation with the right amount of caution instead of pretending the signal is complete.

## Minimum Report Contract

Every report should include:

- Location orientation summary
- Purpose lens
- Aspect signal snapshot
- Catchment interpretation
- Surrounding ecosystem interpretation
- Movement and last-mile interpretation
- Time-based character
- Audience/demand signals
- Competition and complementarity
- Ground-reality watchouts
- Future change signals
- Quantified evidence cards
- Source freshness and data limitations written naturally into the report language
- On-ground observation plan
- Nearby comparison prompts

## Terms To Use

Use:

- Supports
- Creates friction
- Suggests
- Indicates
- Watchout
- Unknown
- Signal
- Aspect view
- Natural audience
- Movement pattern
- Exact-pin effect
- Ground observation

Avoid:

- Verdict
- Proceed
- Avoid
- Invest
- Do not invest
- Buy now
- Reject
- Guaranteed
- Best location
- Will succeed

## Default Runtime Flow

1. Parse and normalize the location.
2. Ask for purpose and sub-purpose using `input-taxonomy.yaml`.
3. Ask only the extra context fields needed for that purpose.
4. Build distance rings and travel-time catchments.
5. Collect signals from maps, POIs, mobility, reviews, civic, environmental, infrastructure, future-development, and public-web gold consumer surfaces where relevant to the purpose.
6. Convert raw observations into quantified evidence cards.
7. Create aspect panels using the selected purpose module.
8. Generate interpretations with quantified support, source-aware limitations, and linked references.
9. Assemble the report using `master-report-template.md`.
10. Validate structured output against `output-schema.json`.
11. End with an on-ground observation plan.

## Good Output Example

Weak:

```text
This is a good location for a cafe because there are colleges and offices nearby.
```

Strong:

```text
The 1 km catchment shows a student and young-professional signal: 3 education anchors, 2 office clusters, and 18 food/beverage POIs were found within the relevant rings. This supports weekday evening cafe usage. The exact pin still needs footfall validation because the immediate 300 m stretch has fewer dwell-time POIs than the broader locality.
```

## Source Anchors

Public and open anchors that can support the report engine include:

- Mappls Search / Geocoding / POI: https://about.mappls.com/api/search-and-geocoding
- Google Maps Platform Geocoding / Places / Routes: https://developers.google.com/maps/documentation
- HERE Geocoding, Search, Routing, and Traffic: https://docs.here.com/
- Overture Maps Places and Addresses: https://docs.overturemaps.org/
- Census of India Primary Census Abstract: https://censusindia.gov.in/nada/index.php/catalog/6191
- Census town/village/ward datasets: https://censusindia.gov.in/nada/index.php/catalog/study/PC11_PCA-TV-0505
- Open Government Data Platform India APIs: https://www.data.gov.in/apis/
- CPCB National Air Quality Index: https://cpcb.nic.in/national-air-quality-index/
- India Meteorological Department rainfall information: https://mausam.imd.gov.in/responsive/rainfallinformation.php
- Bhuvan thematic maps: https://bhuvan.nrsc.gov.in/wiki/index.php/Thematic_Data
- NRSC Flood Hazard Zonation Atlas: https://www.nrsc.gov.in/nrscnew/resources_atlas_FloodHazard_Zonation.php
- OpenStreetMap Overpass API: https://wiki.openstreetmap.org/wiki/Overpass_API
- PhonePe Pulse data API: https://www.phonepe.com/pulse/data-api/
- ONDC public ecosystem data: https://ondc.org/
- Zomato locality delivery surfaces, for example: https://www.zomato.com/pune/delivery-in-hinjewadi
- Blinkit locality-conditioned catalog: https://blinkit.com/
- Zepto locality-conditioned catalog: https://www.zepto.com/
- Playo venue discovery: https://playo.co/
- Hudle venue discovery: https://www.hudle.in/
- KheloMore venue discovery: https://www.khelomore.com/
- Mapillary imagery and detections: https://help.mapillary.com/hc/en-us/articles/360010234680-Accessing-imagery-and-data-through-the-Mapillary-API
- Delhi Open Transit Data GTFS documentation: https://otd.delhi.gov.in/documentation
- GTFS reference: https://gtfs.org/
