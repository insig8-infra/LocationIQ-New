# LocationIQ S2Vec-Inspired Location Embeddings

Version: 0.1  
Date: April 28, 2026  
Status: Build-start draft

## 1. Purpose

LocationIQ should include an internal location-character layer inspired by Google Research's S2Vec work.

This layer should help the product understand the built-environment character around a selected pin before and during report generation.

It should support:

- low-cost preview generation,
- source planning,
- report personalization by use case,
- similar-location retrieval,
- tier 2 / sparse-data robustness,
- internal QA and contradiction checks.

It should not become a user-facing proof source by itself.

## 2. Research Basis

Google Research introduced S2Vec as a self-supervised geospatial embedding framework for the built environment.

Core idea:

```text
S2 cells + built-environment feature vectors + rasterization + masked autoencoding = location embeddings
```

Useful references:

- Google Research blog: https://research.google/blog/mapping-the-modern-world-how-s2vec-learns-the-language-of-our-cities/
- arXiv paper: https://arxiv.org/abs/2504.16942
- S2 Geometry: https://s2geometry.io/
- S2 cell statistics: https://s2geometry.io/resources/s2cell_statistics.html

Important interpretation for LocationIQ:

- S2Vec is a research framework, not currently a normal Google Maps API product.
- We should build our own LocationIQ version using our India-first source stack.
- The useful concept is the embedding architecture, not dependency on Google's internal data.

## 3. Product Role

The embedding layer should answer internal questions like:

- What type of place is this exact pin in?
- Is the surrounding cell office-heavy, residential-heavy, mixed-use, sparse, highway-led, or institutional?
- Which source families should the full report prioritize?
- Does this location resemble other known locations?
- Does the generated narrative contradict the mapped built-environment profile?

It should not directly answer:

- Should the user buy/open/invest?
- Is demand certain?
- Is the plot physically suitable?
- Is the area rich, safe, clean, or premium without other evidence?

## 4. Multi-Resolution S2 Cell Strategy

Google's paper uses S2 cells as the spatial backbone. LocationIQ should do the same, but at multiple resolutions because our product is exact-pin-first.

| S2 level | Approx role for LocationIQ |
|---|---|
| L16 | Immediate micro-context around the pin. |
| L15 | Block or very-near-neighborhood character. |
| L14 | Walkable/local pocket character. |
| L13 | Locality submarket context. |
| L12 | Broader 3-5 km style built-environment context. |

S2 Geometry official statistics show level 12 cells average around 5 sq km, while finer levels get down to neighborhood and block-like scale. Exact edge length varies by location.

For every report request, store:

```text
s2_l16
s2_l15
s2_l14
s2_l13
s2_l12
```

The selected coordinate remains canonical. S2 cells are analytical context.

## 5. Feature Vector Design

LocationIQ should compute cell-level feature vectors from our source stack.

### 5.1 Core Built-Environment Features

Feature families:

- POI counts by category.
- POI roles: demand anchor, competitor, complement, friction source, support service.
- Road class counts.
- Road density.
- Intersection density.
- Transit stop count.
- School / college / coaching count.
- Hospital / clinic / pharmacy count.
- Office / coworking / business park count.
- Residential society / project count.
- Retail / market / mall count.
- Cafe / restaurant / food density.
- Gym / sports / recreation count.
- Religious / community anchor count.

### 5.2 Public-Web Gold Features

Where source collection is stable and locality-conditioned:

- Zomato/Swiggy listing count.
- Food category/cuisine mix.
- Visible price-band distribution.
- Blinkit/Zepto serviceability and category breadth.
- Playo/Hudle/KheloMore venue count.
- Booking slot count.
- Visible booking price records.
- Normalized price bands where available.

### 5.3 Access And Movement Features

- Distance to arterial road.
- Route complexity to main road.
- Transit stop count.
- Travel-time bands to major anchors.
- Peak/non-peak travel delta.
- Last-mile friction cues where available.

### 5.4 Future And Official Context Features

- RERA project count.
- Metro/road/project proximity.
- Official infrastructure project count.
- Construction/change signals.
- Census or settlement baseline where useful.

### 5.5 Features To Keep Separate

Do not collapse these into unsupported user-facing claims:

- hyperlocal safety,
- cleanliness,
- noise,
- waterlogging,
- exact parking capacity,
- physical suitability,
- legal parcel suitability.

These can be auxiliary features only when reliable evidence exists.

## 6. Embedding Pipeline

LocationIQ should build this in two stages.

### 6.1 Stage A: Deterministic Cell Profiles

Build from day one.

For each S2 cell:

1. Collect normalized observations.
2. Aggregate counts, densities, and proportions.
3. Store a feature vector.
4. Generate a human-readable internal profile.

Example internal profile:

```json
{
  "s2_level": 15,
  "cell_id": "s2_...",
  "profile_labels": [
    "office_residential_mixed",
    "sports_leisure_visible",
    "car_two_wheeler_access_dependent"
  ],
  "top_features": [
    "high office anchor count",
    "visible sports venues",
    "moderate food support ecosystem"
  ],
  "data_limit_note": "Public-web sports data is locality-level, not exact-pin demand."
}
```

This stage does not require ML training and should be included in the first build.

### 6.2 Stage B: Self-Supervised Embeddings

Build once enough India-wide feature data exists.

Approach:

1. Choose parent image cell level and child patch cell level.
2. Generate feature vector per child S2 cell.
3. Rasterize child feature vectors into parent-cell grids.
4. Train masked autoencoder to reconstruct masked cells.
5. Store embeddings per S2 cell in Supabase pgvector.
6. Evaluate against downstream tasks and report-quality QA.

Do not block V1 on full model training. But design schema and pipeline from day one so this can be added without refactor.

## 7. Internal Uses

### 7.1 Low-Cost Preview

Use cell profiles to create a useful preview before payment.

Example:

```text
This pin sits in a mixed office-residential pocket with visible sports and food-support activity nearby. The full report will check whether that broader locality strength applies to the exact pin.
```

Preview must still avoid final verdicts.

### 7.2 Source Planning

Use the profile to prioritize source families.

Example:

| Profile signal | Source planning impact |
|---|---|
| sports/leisure visible | Prioritize Playo, Hudle, KheloMore, Google Places sports categories. |
| food-support dense | Prioritize Zomato/Swiggy and restaurant POI mix. |
| sparse peri-urban | Prioritize routing, satellite/change, official future-development sources. |
| residential-heavy | Prioritize daily needs, schools, healthcare, quick commerce, commute. |
| office-heavy | Prioritize evening access, food support, parking/drop-off, weekday traffic. |

### 7.3 Similar-Location Retrieval

Use embeddings to find similar cells/locations.

Internal use:

- QA against known examples.
- Build comparison benchmarks.
- Detect whether the selected pin resembles successful or weak site patterns.
- Recommend which report modules need extra attention.

User-facing output should be careful:

```text
The built-environment pattern around this pin is closer to an office-residential edge than a pure residential pocket.
```

Avoid:

```text
The embedding says this location will work.
```

### 7.4 Tier 2 Robustness

In smaller cities or sparse localities, cell profiles can keep reports structured when public-web gold data is thin.

Rules:

- Use embeddings to guide what to investigate.
- Do not use embeddings as evidence for demand.
- Tell the user when evidence is sparse.

### 7.5 QA And Contradiction Detection

Use cell profile to detect report drift.

Examples:

- Report says "office-led pocket" but cell profile has very low office/coworking/business POI count.
- Report says "food-support dense" but public-web and POI food signals are weak.
- Report uses one sports anchor but cell profile has no broader sports/leisure signal.

Flag these before report release.

## 8. User-Facing Language Rules

Do not expose raw embedding scores.

Do not say:

- "S2Vec score"
- "embedding cluster"
- "model classified this area as..."
- "AI predicts..."

Use natural language:

- "The mapped built-environment pattern around the pin looks..."
- "The immediate cell is more residential-support than office-led..."
- "This is a locality-level pattern, not exact-pin proof..."
- "The broader area has the shape of..."

Every user-facing interpretation still needs source-backed numbers or clear limitation wording.

## 9. Data Model Requirements

Add these tables:

- `s2_cells`
- `s2_cell_features`
- `s2_cell_embeddings`
- `location_cell_profiles`
- `similar_location_matches`

The API/data model spec defines the table-level details.

## 10. Build Requirements

V1 must include:

- S2 cell IDs for every selected pin.
- Deterministic cell profiles for selected pin cells.
- Cell profile usage in low-cost preview.
- Cell profile usage in source planning.
- Cell profile audit display in admin tooling.

Post-V1 / model-training phase:

- Masked-autoencoder training pipeline.
- Stored cell embeddings.
- Similar-location retrieval.
- QA contradiction detector.
- Evaluation across pan-India, tier 1, tier 2, and peri-urban samples.

## 11. Acceptance Criteria

The S2/location-character layer is ready for build when:

- every location stores S2 cell IDs for L12-L16,
- cell feature vectors can be generated from normalized observations,
- preview can use deterministic cell profile labels,
- source planner can consume cell profile labels,
- embeddings are stored in pgvector-compatible format when available,
- user-facing report never treats embeddings as proof,
- admin view can show profile labels, feature vector summary, and similar-location matches.
