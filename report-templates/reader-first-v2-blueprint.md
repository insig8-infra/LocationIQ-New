# Reader-First V2 Report Blueprint

Status: historical reference only.

This file is retained to preserve the evolution of the product thinking. The current production direction for the technical spec is `reader-first-v4-blueprint.md`, `master-report-template.md`, `purpose-modules.md`, `india-signal-library.md`, `input-taxonomy.yaml`, and `output-schema.json`.

This blueprint upgrades the report from "clear and smart" to "decision-grade for a first-time reader."

The goal is not to make the report more technical. The goal is to make the user feel:

- I can picture this place.
- I understand why the report is saying this.
- I can compare it against alternatives.
- I know what still needs to be checked in person.

## Why V2 Exists

The current report language direction is good: it is plain-English, interpretive, and not overly analyst-heavy.

What it still under-delivers for a layman:

- too little visual grounding
- not enough quantified support behind important claims
- weak mental picture of the exact pin
- limited competitive comparison at a glance
- insufficient separation of fact, interpretation, and field uncertainty

V2 solves that by adding visual blocks, numeric blocks, and a more explicit reading structure.

## Core V2 Rule

Every major section should answer these three things in order:

```text
1. What did we observe?
2. What does that likely mean for this purpose?
3. What still needs physical verification?
```

This is the single best trust-building structure for a layman.

## Copy Discipline

The report must never talk to itself.

Avoid body copy like:

- "this section tells you"
- "the v2 structure is"
- "as a layman"
- "this report is designed to"
- "the current report is stronger when"

Use user-facing framing instead:

- "What this means for you"
- "What you should pay attention to"
- "What you are likely to experience"
- "What you still need to verify in person"
- "Why this matters for your decision"

The report should sound like a sharp local guide speaking to the user, not like a product manager describing the interface.

## Exact-Pin Discipline

Exact-pin accuracy is non-negotiable.

The canonical source of truth is the input coordinate, not the nearest named POI.

The system must:

1. preserve the raw coordinate as the primary identity
2. reverse-geocode the exact point
3. find nearby POIs with exact distances
4. classify the relationship between the pin and nearby POIs
5. avoid naming the pin as a business unless the geometry and distance justify it

Recommended pin relationship labels:

- `on_poi`
- `inside_poi_boundary`
- `adjacent_to_poi`
- `across_from_poi`
- `between_pois`
- `unlabeled_plot_near_poi`

Bad output:

```text
The pin is The Pickle Point
```

when the point is actually beside it.

Good output:

```text
The pin appears to fall on an adjacent sports plot beside The Pickle Point and near V J Sports Club.
Use those operators as nearby reference evidence, not as the pin identity itself.
```

If map surfaces disagree, the report should say so explicitly instead of pretending certainty.

## Map Layer Rule

For production India-first UI, the primary user-facing map layer should be Google Maps.

Use Google Maps for:

- base navigation context
- reverse geocoding
- place identity checks
- routing and travel-time
- Street View or nearby imagery
- user trust surface

Sample reports may temporarily use placeholder or alternate embeds, but they must be labeled clearly as sample-only.

## Price Normalization Discipline

Never compare raw public sports prices unless the unit is normalized.

Teaser prices on consumer platforms may represent:

- 30-minute slot
- 60-minute slot
- 90-minute slot
- court booking
- per-player booking
- weekday price
- weekend price
- prime-time surcharge

Before presenting a comparison ladder, the product should normalize into one or more standard units:

- `Rs per court-hour`
- `Rs per player-hour`
- `weekday peak`
- `weekday non-peak`
- `weekend peak`

If the unit cannot be normalized confidently, the report may still show it as a teaser-price surface, but it must say:

```text
These are public first-view prices and are not directly comparable yet.
```

The report must never turn mixed-duration teaser prices into a fake ranked comparison.

## Nearby Example Discipline

Food, retail, and leisure examples must be:

- active
- actually nearby the selected pin or locality-conditioned surface
- fresh enough to trust
- relevant to the purpose

Do not use examples that are:

- shut
- replaced
- clearly too far from the pin
- weakly connected through a loose city-level search

If freshness or nearness is uncertain, remove the named example and keep the interpretation at the locality-surface level.

## V2 Report Contract

Every V2 report should include all of the following:

1. One-screen summary
2. Exact-pin map and broader catchment map
3. Key numbers strip
4. Audience/catchment picture
5. Access and arrival understanding
6. Competition comparison table
7. Price and positioning visuals
8. Time-of-day demand visual
9. Visual evidence or screenshots
10. Friction and watchout section
11. Field visit checklist
12. Evidence confidence and data limitations

## V2 Section Order

Use this section order by default unless a purpose module has a strong reason to reorder.

### 1. Report Header

Must show:

- report title
- purpose lens
- normalized location
- coordinates
- generated date
- data freshness note

### 2. One-Screen Summary

This is the new first screen.

It should contain:

- one plain-English location character line
- 3 to 5 "read this first" insight cards
- strongest signals
- biggest friction signals
- what still needs site visit proof

Good output shape:

```text
What looks strong
What may frustrate users
What kind of spending behavior is visible
What this place feels like in one sentence
```

### 3. Exact-Pin Visual Orientation

This section should help the user picture the exact site immediately.

Preferred outputs:

- embedded map or annotated static map
- exact-pin schematic
- numbered landmark legend
- immediate 100 m / 300 m explanation

Mandatory callouts:

- exact pin
- entry road
- nearest road edge or gate
- major nearby landmark
- nearest residential or office anchor
- relevant support uses

### 4. Broader Catchment Visual

Show the area in layers:

- 300 m
- 1 km
- 3 km
- 5 km or 10-15 min travel

Preferred visual formats:

- catchment rings on map
- travel-time map
- side-by-side locality map

This section should answer:

```text
Who can realistically reach this location, and from what kind of surrounding environment?
```

### 5. Key Numbers Strip

This is mandatory in V2.

The layman needs immediate numeric anchors.

Examples:

- rating
- review count
- visible competitor count
- price range
- demand timing signal
- distance or travel-time benchmarks
- venue count in search results
- booking-price range

Rules:

- numbers must be source-backed
- do not invent precision
- if a number is approximate, label it clearly

### 6. Audience Picture

This section should make the surrounding human market feel real.

Possible audience groups:

- residents
- office workers
- students
- families
- visitors
- existing hobby/sports users

Preferred evidence:

- township or residential anchors
- office park anchors
- public sports-booking evidence
- review language themes
- food and leisure spending surfaces

Preferred visual shapes:

- audience cards
- catchment matrix
- segment bars

### 7. Access And Arrival

This section is often under-explained today and should become a first-class block.

Must answer:

- how people approach the site
- where they are likely to get delayed
- whether the final entry is obvious or confusing
- whether a first visit feels easy or tiring
- whether parking/drop-off is likely to become a pain point

Preferred outputs:

- route map
- arrival friction diagram
- benchmark travel-time table
- weekday vs weekend difference note

### 8. Competition Comparison Table

This is one of the highest-value V2 additions.

Every report should include a comparison table with columns like:

| Place | Distance / travel time | Price | Rating / reviews | Key amenities | Format | Why it matters |
|---|---|---:|---|---|---|---|

Purpose modules can override columns.

For example:

- home buying: society / micro-market comparison
- cafe: direct and indirect substitutes
- pickleball: nearby bookable courts and sports clusters

### 9. Price And Positioning Visuals

V2 should not only state price clues in text. It should show them visually.

Preferred formats:

- price ladder bars
- price band chart
- nearby leisure spend vs everyday spend split
- visible competitor pricing ladder

Examples:

- Zomato price for two
- Zomato price per person
- Hudle / Playo booking prices
- quick-commerce basket clues where relevant

### 10. Time-Based Demand Visual

This section should convert time-based interpretation into something the user can scan fast.

Preferred visuals:

- hourly bar chart
- weekday/weekend heat grid
- daypart table

Use this for:

- Google popular-times snapshots
- booking-slot patterns
- locality activity patterns
- opening-hour overlaps

### 11. Visual Evidence Block

This is mandatory when strong imagery exists.

Preferred evidence types:

- map screenshots
- street-view screenshots
- approach-road screenshots
- venue photos
- public platform images
- annotated aerial views

For downloadable reports:

- include still screenshots

For web reports:

- interactive embeds are allowed

Rules:

- visuals must improve understanding, not decorate
- avoid generic stock images unless clearly separated from evidence

### 12. Friction And Watchouts

This section should show what could disappoint the user even if the catchment is strong.

Good V2 structure:

- friction type
- what evidence suggests it
- why it matters for the purpose
- what would confirm it on the ground

Examples:

- traffic and access
- monsoon behavior
- parking spillover
- civic cleanliness
- odor/noise
- after-dark comfort
- operator-dependence versus location strength

### 13. What To Check In Person

This should become more operational in V2.

Do not stop at generic advice.

Specify:

- best time windows to visit
- what to count
- what to photograph
- what to ask locals, guards, vendors, or users
- what would count as a red flag
- what would count as a strong positive signal

Good output shape:

| Visit window | What to observe | What would be a red flag | What would be reassuring |
|---|---|---|---|

### 14. Evidence Confidence

The current confidence section is directionally right. V2 should make it even clearer.

Use these buckets:

- directly observed from current source
- strongly supported by multiple sources
- interpreted from proxy evidence
- still needs field proof

## V2 Visual Component Library

These reusable blocks should be available to the report renderer.

### Mandatory reusable blocks

- metric tiles
- annotated map panel
- catchment map panel
- price ladder chart
- demand timing bar chart
- competition table
- field-check table
- confidence legend

### Nice-to-have reusable blocks

- route comparison strip
- evidence image gallery
- review-theme chips
- exact-pin versus broader locality comparison panel

## Quantification Rules For V2

V2 should aggressively prefer numbers where they increase trust.

Good examples:

- 4.8 stars from 102 reviews
- 80 venues surfaced on a city/locality booking page
- Rs 175 to Rs 800 visible booking ladder
- 6 PM to 11 PM visible demand curve
- 5 named competitors within the broader corridor

Bad examples:

- "many competitors"
- "good demand"
- "affluent area"
- "nearby audience"

without any numeric support.

## Visual Honesty Rules

If a visual is:

- schematic
- approximate
- manually annotated
- based on pin reading rather than parcel-level GIS

say so clearly.

If the product later has production-grade GIS and imagery, replace the schematic view with exact rendered maps.

## Purpose Adaptation Notes

All purposes should use the same V2 grammar, but the visuals should adapt.

### Pickleball / sports venue

Highest-value V2 visuals:

- pin map
- competitor map
- price ladder
- peak-hour usage chart
- amenity comparison table
- arrival friction diagram

### Home buying / apartment

Highest-value V2 visuals:

- daily-needs map
- commute map
- schools/healthcare map
- environment and flooding map
- neighborhood comparison table
- street-view evidence panel

### Cafe / franchise / retail

Highest-value V2 visuals:

- frontage and access map
- demand-anchor map
- competitor cluster table
- daypart chart
- spending ladder
- walk-in versus delivery catchment view

## Production Implication

If the app is meant to feel clearly better than a plain AI summary, V2 is not optional.

The winning difference is not only better writing.

It is:

- stronger visual grounding
- stronger quantified support
- clearer comparison
- better explanation of uncertainty
- better field-visit guidance

## Short Version

The V2 report should feel like:

```text
a guided location walkthrough with maps, numbers, comparisons, and field prompts
```

not just:

```text
a smart written interpretation
```
