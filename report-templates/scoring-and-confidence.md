# Aspect Signals, Source-Aware Language, And Data Limits

This file keeps its historical filename, but the current v4 direction is not to show certainty badges or source-quality labels in the user-facing report.

LocationIQ should produce purpose-aware aspect signals backed by numbers, sources, and clearly worded limits. It should not produce a final decision verdict.

## No Overall Verdict

Do not compute or display:

- Overall score
- Final verdict
- Proceed/avoid label
- Investment rating
- Buy/open recommendation

If engineering needs internal ranking or retrieval scores, keep them internal. They should not become the user's answer.

## User-Facing Aspect Signals

The report can still show aspect-level signal language when it helps scanning.

Allowed labels:

| Label | Meaning |
|---|---|
| Strong supportive signal | Multiple current signals point in the same helpful direction for the selected purpose. |
| Supportive signal | Available indicators are directionally helpful. |
| Mixed signal | Useful and friction signals are both present. |
| Friction signal | A meaningful practical challenge is visible. |
| Weak signal | The visible evidence does not strongly support the aspect. |
| Unknown | Data is too sparse, stale, or conflicting to interpret responsibly. |
| Not relevant | The aspect is not important for the selected purpose. |

Avoid showing a numeric aspect score unless there is a strong product reason. If an index is used internally, it must not be presented as a final outcome.

## Internal Data Quality

Internal systems may compute data-quality metadata for retrieval, generation, QA, and audit.

Useful internal dimensions:

```yaml
data_quality:
  source_reliability: 0_to_5
  source_recency: 0_to_5
  spatial_precision: 0_to_5
  source_agreement: 0_to_5
  repeatability: 0_to_5
  data_density: 0_to_5
```

Do not surface these as `High/Medium/Low` badges in the report body.

Instead, convert them into natural language:

- "The latest available official source says..."
- "Public booking pages currently show..."
- "This is a locality-level signal, not exact-pin proof..."
- "This source appears older, so treat it as background context..."
- "This could not be verified from a reliable public source in this pass..."

## Quantified Evidence Rules

Whenever possible, important claims should include at least one number.

Good:

```text
Playo's Hinjawadi pickleball surface currently lists 80 results, including venues, coaching, events, and memberships. This indicates platform-visible category activity, but it should not be treated as total market size.
```

Weak:

```text
The area has good demand.
```

Minimum internal evidence shape:

```yaml
id: "signal_001"
metric_name: "visible_pickleball_results"
value: 80
unit: "platform_results"
area: "Hinjawadi locality page"
source_type: "public_web_gold"
source_url: "https://playo.co/venues/hinjewadi-pune/sports/pickleball"
last_checked: "2026-04-25T17:00:00+05:30"
user_facing_source_note: "Playo currently surfaces 80 Hinjawadi pickleball results; this is platform visibility, not total market size."
limitations:
  - "Platform results may include coaching, events, memberships, and venues."
  - "Ranking and availability may change."
```

## Public-Web Gold Rules

Use locality-conditioned public-web evidence only when all of the following are true:

- the selected pin can be mapped to the platform-visible locality or catchment,
- the capture reflects that locality rather than a generic city page,
- the fields extracted are visible and repeatable enough to interpret,
- the report says what the signal does and does not prove.

Good public-web gold sources by use case:

- Playo, Hudle, KheloMore for sports discovery, slot visibility, amenities, and pricing units
- Zomato and Swiggy for locality-conditioned food surfaces
- Blinkit, Zepto, Instamart for serviceability and convenience-depth cues
- Google Maps / Places for POIs, ratings, reviews, photos, hours, and routing context

Public-web gold is strong for visibility, competition, convenience, and category-activity signals. It is not direct transaction truth unless transaction data is explicitly available.

## Pricing Normalization

Do not compare public sports prices until slot units are normalized.

Capture:

- platform
- venue
- sport
- date checked
- start time
- end time
- slot duration
- price
- price unit: court, player, session, event, membership
- weekday/weekend
- peak/non-peak
- indoor/outdoor
- included add-ons where visible

Normalize:

- Rs per court-hour
- Rs per player-hour only where player pricing is explicit
- separate peak and non-peak bands
- separate normal rental, coaching, tournament, event, glow, and subscription prices

If duration or unit is missing, write:

```text
The public price is visible, but it is not comparable yet because the slot unit was not captured.
```

## Exact-Pin Discipline

The selected coordinate is canonical. Nearby POIs are context.

Do not:

- rename the selected pin after the nearest business,
- claim a legal plot boundary from a visual map outline,
- infer plot ownership or permissions,
- claim how many courts fit,
- claim drainage, lighting, or parking capacity from remote data alone.

Do:

- show the exact marker,
- show nearby operators and land use,
- show a visual plot highlight only when clearly labeled as non-legal,
- tell the user what to verify physically.

## Multi-Anchor Interpretation

No single source or single nearby venue should carry the demand story unless the selected pin is exactly that venue.

For sports and leisure reports, combine:

- exact-pin context,
- adjacent operator evidence,
- same-category competitor surfaces,
- audience anchors,
- access and arrival data,
- spend and convenience surfaces,
- time-window signals.

If only one anchor exists, write that the signal is narrow.

## Competition Language

Use observable facts:

- distance and travel time,
- indoor/outdoor,
- public amenities,
- hours,
- rating/review count,
- platform presence,
- slot visibility,
- normalized price.

Avoid unsupported statements about:

- crowd type,
- market gaps,
- premium/cheap positioning,
- who will win,
- user intent,
- operator quality.

If a review-theme analysis is available, mention the sample size and the source family. If not, keep the language factual.

## India-Realistic Locality Quality

Use only signals that can be retrieved reliably enough for the pin and city.

Usually reliable:

- routing and travel-time data,
- POIs, reviews, hours, and photos,
- public booking and consumer surfaces,
- official infrastructure/project pages,
- CPCB station/city-level AQI,
- IMD weather/warnings where accessible,
- dated local news,
- user or field observations.

Often uneven:

- hyperlocal cleanliness,
- night safety,
- exact parking capacity,
- waterlogging at plot level,
- road surface quality,
- noise,
- encroachment.

When uneven, use field-check wording rather than a score.

## Language Guidelines

Use:

- "currently shows"
- "public pages list"
- "available indicators suggest"
- "this is locality-level"
- "this needs a site visit"
- "treat this as a cue, not proof"
- "not normalized yet"

Avoid:

- "guaranteed"
- "definitely"
- "best"
- "must buy"
- "should invest"
- "will succeed"
- "direct evidence badge"
- "weak proxy badge"
- "certainty score" in user-facing copy

The user-facing report should feel readable, sourced, and honest without making the source framework the main experience.
