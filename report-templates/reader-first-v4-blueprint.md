# Reader-First V4 Blueprint

This blueprint supersedes the V2 sample direction for reports that need to feel useful to a common buyer or small business owner. The report should still be simple to read, but it must be more visually grounded, more careful with source language, and more realistic about what can be known from Indian data.

Core idea:

```text
Do not make the report look like a proof dossier.
Make it feel like a clear, source-aware location story.
```

## 1. Source Language

Do not label every statement as `direct`, `inferred`, or `weak proxy` in the UI. That turns the report into an audit sheet.

Instead, write source quality into the sentence naturally:

- "Google Maps currently resolves the coordinate near..."
- "Public booking pages for nearby venues show..."
- "The latest available official source says..."
- "This source appears older, so treat it as background context..."
- "Recent public reviews mention..."
- "The data is locality-level, not exact-pin level..."
- "This could not be verified from a reliable public source in this pass..."

Rules:

- Every important number should still link to a source.
- Source links should sit gracefully inside the text, table row, caption, or footnote.
- Do not create a separate proof block for every claim.
- If a claim depends on stale, partial, or proxy data, the wording must make that clear.
- If a source is not reliable enough for the user-facing report, do not surface the claim.

## 2. Exact Pin And Plot Truth

The exact coordinate is canonical. The nearest named POI is not canonical.

The product should separate:

- exact coordinate
- reverse-geocoded address or plus code
- nearest visible POIs
- likely parcel or plot envelope
- legal cadastral boundary, only when verified

What can be highly accurate:

- exact lat/lng marker
- reverse geocode
- nearby named places
- road approach
- satellite-level visual context
- highlighted map viewport around the selected pin
- approximate visual plot area when visible on satellite imagery

What should not be claimed unless verified:

- legal plot boundary
- plot ownership
- parcel size
- permissible commercial use
- court-fit feasibility
- exact frontage width

Production approach:

- Use Google Maps for the primary user-facing map, reverse geocoding, nearby places, routing, Street View, and screenshots.
- Use Google Maps Static API or Maps JavaScript API to show a zoomed map with marker, labels, and optional path/polygon overlays. Google documents marker, map type, viewport, and path support for Maps Static API: https://developers.google.com/maps/documentation/maps-static
- Use Google Places API for nearby POI discovery and place detail enrichment: https://developers.google.com/maps/documentation/places/web-service
- Use official cadastral or licensed parcel sources only when available. For Maharashtra, Mahabhumi lists Mahabhunakasha under land-record map services: https://mahabhumi.gov.in/mahabhumilink
- If cadastral geometry is unavailable or cannot be reliably joined to the pin, call the overlay "visual plot area" or "likely plot envelope", not "legal plot boundary".

Report visual:

- Show the exact pin on a zoomed satellite map.
- Highlight the likely visual plot area in a distinct color only if the shape is visible or supplied.
- If the boundary is not verified, caption it clearly: "visual highlight, not legal boundary".
- Add adjacent labels: road edge, entry side, nearest operators, residential edge, open land, parking/approach clue.

## 3. Internal Evidence Layers

The generation pipeline should track which layer supports each conclusion, but the report should not make the layers the main UI.

Internal layers:

- exact pin and reverse geocode
- adjacent operators and land use
- same-category competitors
- audience anchors
- access and travel-time friction
- spend and convenience signals
- locality condition signals
- field verification needs

User-facing treatment:

- Weave the layers into natural sections.
- Use captions, compact source links, and "what this means for you" language.
- Do not make the user feel they are reading a legal evidence bundle.

## 4. Multi-Anchor Demand Model

Never let one nearby venue carry the demand story unless the selected pin is exactly that venue.

For a sports or leisure business report, demand should be built from a basket:

- exact pin context
- adjacent operator evidence
- same-category competitor surface
- nearby residential anchors
- nearby office or institution anchors
- food, cafe, quick-commerce, and leisure spending cues
- time-of-day signals from multiple sources where possible

If only one anchor exists, do not generalize. Say the signal is narrow.

Bad:

```text
V J Sports Club is busy at 7 PM, so the whole cluster has strong evening demand.
```

Better:

```text
One nearby sports anchor shows evening activity on Google Maps, while adjacent pickleball booking pages and the broader Playo/Hudle inventory suggest this is not a single-venue pocket. The exact plot still needs an evening visit because the public timing signal is not plot-specific.
```

## 5. Visual Standard

The report should make the user picture the place without heavy imagination.

Preferred visuals:

- zoomed exact-pin satellite map with highlighted visual plot area
- broader catchment map with 5, 10, and 15 minute drive-time rings
- competitor map with distance and category labels
- arrival sequence map: main road, final turn, entry, drop-off, parking clue
- Street View or approach screenshots in available directions
- price normalization table and chart
- source screenshots only where allowed and useful
- field-visit photo checklist

Avoid:

- rudimentary hand-drawn SVGs as the main map evidence
- decorative diagrams that do not add decision value
- fake precision
- screenshots or visuals that are not tied to a user question

If a sample cannot use live Google imagery, the sample may use a designed mock visual, but it must be labeled as a sample visual. Production reports should use real map tiles, satellite imagery, Street View, platform screenshots, or user-uploaded photos where permitted.

## 6. Physical Suitability Boundary

Do not make physical suitability a report concern unless reliable dimensional or field data exists.

The report should not claim:

- how many courts fit
- whether drainage is adequate
- whether lighting can be installed
- whether the plot is legally or physically suitable
- whether parking capacity is sufficient

The report can say:

- what must be checked on site
- what visual clues are visible from maps or photos
- what users may experience on arrival
- what evidence is missing before judging the site

For business owners, the report should support a better site visit, not replace due diligence.

## 7. Competition Depth Without Made-Up Claims

Competition analysis should emphasize observable facts:

- venue name
- distance and travel time
- indoor or outdoor
- number of courts, if available
- amenities shown publicly
- hours
- rating and review count
- bookable slot availability
- normalized price
- booking platform presence

Do not infer crowd type, market gaps, or "who wins" unless supported by multiple sources such as review text themes, booking availability, operator positioning, photos, and field evidence.

Acceptable:

```text
Arena X publicly lists parking, washroom, warm-up area, and an upper view deck, so users nearby can compare comfort features, not just court access.
```

Avoid:

```text
Arena X attracts premium serious players.
```

## 8. Normalized Pricing

Pricing should be scraped accurately from KheloMore, Hudle, Playo, and similar platforms where available.

Capture:

- platform
- venue
- sport
- date checked
- start time
- end time
- slot duration
- price
- price unit: court, player, session, subscription, event
- weekday or weekend
- peak or non-peak
- indoor or outdoor
- included rentals, coaching, taxes, fees, or add-ons if shown

Normalize to:

- Rs per court-hour
- Rs per player-hour, only when player pricing is explicit
- prime-time and non-prime-time bands
- weekday and weekend bands

Rules:

- Do not compare prices unless the unit is normalized.
- If slot duration is missing, show the row as "not comparable yet".
- If price is an event, tournament, coaching, or glow format, keep it separate from normal court rental.
- Use screenshots or raw scraped records internally for auditability, but keep the user-facing report clean.

## 9. India-Realistic Locality Quality

Do not add fancy locality attributes because they sound good.

Use only signals that can be retrieved reliably enough for the pin and city.

Usually reliable:

- travel time and traffic from Google Routes API or Distance Matrix style products. Routes API supports routes and route matrices: https://developers.google.com/maps/documentation/routes
- POI and business context from Google Places and public consumer platforms
- official weather, rainfall, forecast, and warnings through IMD APIs where access is approved: https://api.imd.gov.in/
- station or city-level air quality from CPCB AQI surfaces: https://airquality.cpcb.gov.in/AQI_India/
- official planning, metro, road, and public project pages where available
- public booking pages and locality-conditioned consumer surfaces

Often uneven or city-specific:

- hyperlocal waterlogging
- road quality
- cleanliness
- garbage nuisance
- night safety
- noise
- encroachment
- footpath quality
- exact parking capacity

How to handle uneven data:

- show only when a reliable public source, repeated review pattern, official dataset, or field evidence exists
- phrase it as "reported issue" or "visible concern", not a stable locality score
- do not create safety, cleanliness, or nuisance ratings without repeatable source coverage
- if the data is missing, say what should be checked physically

## 10. Final Report Shape

The V4 report should contain:

1. Reader-first opening summary
2. Exact pin and plot visual
3. Multi-anchor location story
4. Catchment and reach
5. Arrival and access reality
6. Numbers that make the story real
7. Competition and normalized pricing
8. Spend and convenience signals
9. Locality conditions, only where reliable
10. Visual evidence pack
11. What to verify physically
12. Source notes woven into the sections, not as the dominant structure

The report should leave the user thinking:

```text
I can see this place clearly. I know what is known, what is only suggested, and what I need to verify in person.
```
