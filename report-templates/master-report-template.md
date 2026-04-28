# Master Interpretive Location Report Template

This is the shared report spine for every LocationIQ report.

The report should not produce a final verdict. It should help the user see the selected location clearly for their purpose, with enough interpretation, visuals, quantified context, and practical field-check prompts to make their own decision.

Current product direction is defined by `reader-first-v4-blueprint.md`.

## Report Principle

Every section should combine:

```text
what is visible + useful numbers + what it may mean for the user's purpose + what still needs checking
```

The report should not feel like a proof dossier. Source quality, freshness, and data limitations should be written naturally into the copy and captions.

Use wording like:

- "Google Maps currently resolves the selected coordinate near..."
- "Public booking pages for nearby venues show..."
- "This is a locality-level signal, not exact-plot proof..."
- "This source appears older, so treat it as background context..."
- "This could not be verified from a reliable public source in this pass..."

Do not use user-facing badges such as `direct`, `inferred`, `weak proxy`, or `evidence strength`.

## 1. Report Header

Include:

- Report title
- Location input
- Exact coordinates
- Reverse-geocoded address or plus code where available
- Nearest locality
- Purpose category and sub-purpose
- User-selected context
- Generated date/time
- Short data-coverage note written in plain language

Template:

```text
LocationIQ Report: [Sub-purpose] location read for [nearest locality]
Purpose lens: [purpose_category] / [sub_purpose]
Selected pin: [lat, lng]
Nearest locality: [locality, city, state]
Updated: [date/time]
Data note: [plain-language coverage note]
```

Avoid a report-level certainty score.

## 2. Reader-First Opening Summary

This replaces an executive verdict.

Do not say:

- Proceed
- Avoid
- Buy
- Invest
- Open here
- Do not open here

Instead summarize:

- What the place appears to be
- What looks useful for the user's purpose
- What may create friction
- What is known from multiple signals
- What is only suggested or locality-level
- What must be checked physically

Template:

```text
You are looking at [location character]. For [purpose], the useful signals are [signal 1], [signal 2], and [signal 3]. The main thing to check before trusting the location fully is [field check].
```

## 3. Purpose Lens

Explain how the same location is being read through the selected purpose.

Include:

- Purpose category
- Sub-purpose
- User context
- Which aspects matter most
- Which aspects are intentionally excluded

Example:

```text
For a pickleball facility, this report emphasizes repeat sports audience, evening and weekend access, nearby sports discovery surfaces, parking and arrival, weather-day experience, and competing bookable options. It does not estimate profitability, legal suitability, or court-fit feasibility.
```

## 4. Exact Pin And Plot Truth

The exact coordinate is canonical. The nearest named POI is not canonical.

Separate:

- selected coordinate
- reverse geocode
- nearest named places
- likely visual plot area
- legal cadastral boundary, only if verified

What can be shown with high practical accuracy:

- exact marker
- zoomed map/satellite context
- road approach
- adjacent POIs
- Street View or approach screenshots where available
- visual plot highlight if visible or supplied

What should not be claimed unless verified:

- legal plot boundary
- ownership
- parcel area
- commercial permission
- how many courts fit
- drainage adequacy
- lighting feasibility
- parking capacity

Required visual:

- Exact pin map or satellite view
- Marker on selected coordinate
- Nearby labels
- Optional highlighted visual plot area with the caption "visual highlight, not legal boundary" when cadastral data is not verified

## 5. Multi-Anchor Location Story

Do not allow one nearby venue to carry the demand story unless the selected pin is exactly that venue.

Use a basket of anchors:

- exact pin context
- adjacent operators and land use
- same-category competitors
- residential anchors
- office/institution anchors
- convenience and leisure surfaces
- access and arrival friction
- time-of-day signals, ideally from more than one source family

User-facing section shape:

| Layer | What is visible | How it should shape your view |
|---|---|---|
| Exact pin | [coordinate and immediate context] | [why the exact pin matters] |
| Adjacent operators | [nearby public surfaces] | [what they suggest, without renaming the pin] |
| Same-category market | [competitor count/listing surface] | [cluster or comparison behavior] |
| Audience anchors | [residential/office/institution anchors] | [likely user routines] |
| Convenience/spend | [food, quick commerce, leisure surfaces] | [spending behavior, not income proof] |

## 6. Catchment And Reach

Use travel-time areas, not only distance rings.

Minimum views:

| Catchment | What to explain |
|---|---|
| Exact pin / 300 m | Arrival, visibility, adjacent context |
| 1 km | Immediate micro-market and convenience |
| 3 km | Strong local catchment |
| 5 km | Broader nearby audience |
| 5/10/15 min travel | Realistic access by relevant mode |

Production reports should use Google Maps / Routes for user-facing travel-time and route views where licensed.

Each catchment section should include useful numbers and a plain-language data note when the signal is locality-level, modeled, or route-time dependent.

## 7. Arrival And Last-Mile Reality

This is a first-class section for Indian locations.

Analyze:

- main access route
- final turn
- last 200-500 m
- parking/drop-off behavior
- cab/auto pickup
- two-wheeler access
- pedestrian comfort where relevant
- night and rain-day arrival

Use field-check wording when remote data cannot prove the condition.

Example:

```text
Map distance makes this location appear close to the office/residential catchment, but the final arrival experience still needs a weekday evening visit. Count parking pressure, drop-off movement, and whether first-time visitors overshoot the turn.
```

## 8. Numbers That Make The Story Real

Show numbers early, but do not overload the report.

Good numbers:

- exact coordinates
- travel time from key anchors
- competitor count
- active booking-surface count
- slot-price units after normalization
- relevant POI counts by catchment
- review count and recency where useful
- official project distance/date where relevant

Rules:

- Link important numbers to sources.
- Do not invent precision.
- Do not compare prices until normalized.
- Do not show stale named examples unless freshness was checked.

## 9. Competition And Pricing

Competition analysis should emphasize observable facts:

- venue name
- distance/travel time
- platform presence
- indoor/outdoor
- hours
- amenities shown publicly
- rating/review count
- bookable slot visibility
- normalized price when available

Do not infer crowd type, market gaps, or who "wins" unless supported by multiple strong sources.

Pricing must be normalized from slot-level data:

- date checked
- platform
- venue
- slot start/end
- duration
- court/player/session unit
- weekday/weekend
- peak/non-peak
- price
- included rentals or add-ons if visible

Normalize to:

- Rs per court-hour
- Rs per player-hour only where player pricing is explicit
- separate prime-time and non-prime-time bands

## 10. Spend And Convenience Signals

Use food, quick-commerce, and leisure surfaces as spending-behavior context, not affluence proof.

Useful sources can include:

- Zomato / Swiggy locality or pin-conditioned restaurant surfaces
- Blinkit / Zepto / Instamart serviceability and catalog depth where collection is repeatable
- Google Places for cafes, restaurants, gyms, sports stores, clinics, and support services

Rules:

- Named examples must be active, nearby, and freshly checked.
- If exact freshness is not verified, use locality-level bands rather than specific restaurant examples.
- Do not call an area "rich" or "premium" without a strong source base.

## 11. India-Realistic Locality Conditions

Only show locality-quality signals that can be retrieved reliably enough.

Usually useful:

- Google routing and travel-time data
- Google Places / public POI context
- official metro/road/project pages
- CPCB station/city-level AQI
- IMD weather/warning data where accessible
- recent local news where specific and dated
- repeated review patterns
- field observations

Often uneven or city-specific:

- cleanliness
- night safety
- hyperlocal waterlogging
- road quality
- noise
- encroachment
- exact parking capacity

If data is uneven, phrase it as a field-check item rather than a score.

## 12. Visual Evidence Pack

Reports should use visuals that answer user questions.

Preferred visuals:

- exact-pin satellite/map view with highlighted visual plot area
- catchment and travel-time map
- competitor map
- arrival sequence map
- Street View / approach screenshots
- normalized pricing chart
- booking availability snapshots where permitted
- field-visit photo checklist

Avoid decorative diagrams that do not increase understanding.

## 13. What To Verify Physically

End with a practical visit plan, not a recommendation.

Include:

- best times to visit
- what to count
- what to photograph
- who to ask
- what contradictions to look for
- purpose-specific checks

Example:

```text
Visit on a weekday between 6:30 PM and 8:30 PM. Count vehicle stacking, observe drop-off movement, photograph the entry and parking edge, and compare the experience after rain.
```

## 14. Source Notes

Do not create a dominant proof register in the report body.

Source links should be woven into:

- section copy
- table rows
- captions
- chart footnotes
- final compact source note

Internal systems can maintain detailed source records for auditability. The user-facing report should stay readable.
