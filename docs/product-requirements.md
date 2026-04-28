# LocationIQ Product Requirements Document

Version: 0.1  
Date: April 25, 2026  
Status: Build-start draft

## 1. Product Summary

LocationIQ is a no-login, paid location intelligence report product for Indian users who are considering a real-world location decision.

The user enters:

```text
location + use case + email
```

LocationIQ shows the pin on a map, asks the user to confirm, gives an impactful low-cost preview, then places the full report behind payment. After payment, the product generates a deep reader-first report, displays progress, opens the report on the page when ready, emails the report link, and later supports a downloadable PDF.

The product does not provide a final buy/open/invest verdict. It helps the user understand and visualize the location from multiple angles so they do not rely only on gut feel.

## 2. Target Users

LocationIQ is designed equally for:

- Common individuals buying or renting a home.
- Small business owners choosing a site.
- Franchise seekers evaluating a store location.
- Operators considering cafes, restaurants, cloud kitchens, gyms, sports facilities, clinics, stores, or similar local businesses.
- People evaluating lesser-known or unfamiliar areas in India.

The product should feel usable by a non-technical person and valuable to someone who already knows the city but not the exact pin.

## 3. Geography

Launch posture:

```text
Pan-India from day 1
```

The product must handle:

- Metros.
- Tier 1 cities.
- Tier 2 cities.
- Fast-changing peri-urban areas.
- Emerging localities where normal Google search is thin.

Quality target:

- Output quality should remain high outside metros.
- If some sources are unavailable for a city, the report should still be useful through alternate source families, official/open data, maps, routing, public-web gold surfaces, and naturally worded data limitations.
- The report should never pad weak areas with generic filler.

## 4. First Use Cases

The first build should support five use-case groups:

| Use-case group | Included examples |
|---|---|
| Home decision | Buy 3BHK, rent home, relocate with family, student/PG housing. |
| Cafe / restaurant / cloud kitchen | Cafe, QSR, restaurant, bakery, cloud kitchen. |
| Sports facility | Pickleball, turf, badminton, box cricket, multi-sport venue. |
| Gym / fitness studio | Gym, yoga studio, pilates, functional fitness, wellness studio. |
| Franchise / storefront | Franchise store, retail outlet, service shop, pharmacy, salon, electronics/fashion store. |

The architecture must remain purpose-extensible, but these five groups define the first golden test suite and report UX.

## 5. User Flow

### 5.1 Entry

The first screen is the product experience, not a marketing landing page.

Required fields:

- Location: Google Maps link, coordinates, address, dropped pin, or landmark.
- Use case: predefined chips plus free-text use case support.
- Email address.

The product should not ask 5-8 extra questions before report generation. The system should infer purpose context where possible and use sensible defaults from the selected use case.

### 5.2 Pin Confirmation

After location entry:

- Resolve the location.
- Show map with exact pin.
- Show nearest locality/address/plus code where available.
- Show a warning if the input resolves only to an area or named place rather than a precise dropped pin.
- Ask the user to click:

```text
Confirm and Analyse
```

The selected coordinate remains canonical.

### 5.3 Low-Cost Preview

After confirmation, show an impactful preview before payment.

Preview goals:

- Build trust.
- Make the user feel the product understands the location and use case.
- Avoid expensive deep source collection.
- Avoid revealing the full value before payment.

Preview can use:

- Already available pin/address/geocode output.
- Precomputed or lightweight S2 cell location-character profile.
- Cached/open map context.
- Light POI summary when low-cost.
- Clear explanation of what the full report will investigate.
- A small number of non-sensitive teaser signals.
- Sample visual modules with blurred/locked sections.

Preview should not require:

- Full public-web gold scraping.
- Deep routing matrices.
- Expensive imagery calls.
- LLM-heavy final report generation.
- Paid vendor calls where avoidable.

Primary CTA:

```text
Get Full Report
```

### 5.4 Payment

After the user clicks `Get Full Report`:

- Create checkout session.
- User pays without creating an account.
- Email is the report delivery identity.
- Payment success starts full report generation.

Payment requirements:

- Payment success must be idempotent.
- The same paid report should not be charged twice if the browser refreshes.
- If payment succeeds but report generation fails, support/admin must be able to retry or refund.
- The report URL should be secure and hard to guess.

### 5.5 Full Report Generation

After payment:

- Show report generation progress on the same page.
- Keep the user informed with stage names that are meaningful.
- Do not make speed the priority over quality.
- Generation can take several minutes.

Progress examples:

- Confirming exact pin
- Reading surrounding map context
- Checking travel-time access
- Finding nearby competitors and anchors
- Checking public platforms
- Normalizing prices
- Building maps and visuals
- Writing your report
- Final quality checks

### 5.6 Delivery

When ready:

- Show the interactive web report on the page.
- Email the report link to the user.
- Provide download option when PDF export is available.

Launch priority:

1. Interactive web report.
2. PDF/download soon after.

### 5.7 No Login

V1 does not require user accounts.

Access model:

- Email + secure report token.
- Optional magic-link style report reopen.
- Admin/support tooling is separate from customer experience.

### 5.8 No Field Visit Loop

V1 does not include user-uploaded photos, field notes, or report update after visit.

The report should still include a strong physical verification plan, but users do not submit that information back into the app in V1.

## 6. Report Product Requirements

Every full report must:

- Preserve exact selected coordinate.
- Explain exact pin vs locality.
- Explain the location through the selected use case.
- Include quantified numbers wherever applicable.
- Use sources and source links gracefully.
- Include maps and visual aids.
- Include public-web gold signals where relevant and reachable.
- Normalize prices before comparing them.
- Include what the user should physically verify.
- Avoid final verdicts and advice labels.

The report voice:

```text
A sharp local expert who knows the hyperlocal area around the pin and is helping the user avoid a gut-only decision.
```

Tone rules:

- Address the user directly as "you".
- Be plain-English and specific.
- Interpret data, do not just dump data.
- Say what a signal means for the user's use case.
- Say what still needs physical verification.
- Do not use internal product language.

## 7. Preview Requirements

Preview must show:

- Exact pin map.
- Resolved location/address/locality.
- Use-case lens.
- Location-character teaser from deterministic S2 cell profile.
- 3-5 preview bullets about what the full report will analyze.
- Example locked sections.
- Expected report modules.
- Payment CTA.

Preview must not:

- Show a final conclusion.
- Surface deep paid-report insights.
- Use stale or fake data.
- Make claims without source/context.

## 8. Data And Source Requirements

The product uses the locked source posture from:

- `/Users/sailsabnis/Insig8/consolidated-sources.md`

Source principles:

- Pan-India quality from day 1.
- Use the best available source family for each signal.
- Use multiple sources when that improves truth.
- Public-web gold surfaces are first-class.
- If high-quality public data is available, the system should collect it.
- The collection must still be pin/locality/catchment-conditioned.
- A public page that a normal user can reach after setting locality, delivery area, city, or venue radius is collectible by default.
- Do not use private/auth-only surfaces as foundational dependencies.
- Do not surface unreliable data just to make the report feel full.

## 9. Functional Scope

In scope for V1:

- Location input with Google Maps link/coordinates/address.
- Use-case input with predefined first five groups.
- Email capture.
- Pin resolution and confirmation.
- S2 cell IDs L12-L16 for every selected pin.
- Deterministic location-character profile for preview and source planning.
- Low-cost preview.
- Payment.
- Async full report generation.
- Interactive report page.
- Email delivery.
- Source-aware report generation.
- Public-web gold collection.
- Pricing normalization.
- Admin retry/support basics.

Soon after V1:

- PDF/download export.
- Stronger admin QA console.
- More use-case groups.
- Vendor QA dashboards.

Out of scope for V1:

- User accounts.
- Saved dashboard for customers.
- Field visit upload loop.
- Manual internal QA before every report.
- Legal, financial, or investment advice.
- Final yes/no recommendations.

## 10. Success Metrics

Product metrics:

- Preview-to-payment conversion.
- Payment success rate.
- Report completion rate.
- Report generation success rate.
- Email delivery success rate.
- Time to completed report.
- Refund/support request rate.
- Repeat purchase by email/domain.
- User feedback rating after report view.

Quality metrics:

- Exact pin confirmation rate.
- Exact pin ambiguity rate.
- S2 cell profile generation success rate.
- Source collection success by city/use case.
- Public-web gold collection success.
- Pricing normalization success.
- Report guardrail failure rate.
- Reports completed with data gaps.
- Admin retry rate.

Trust metrics:

- User reports pin mismatch.
- User reports stale/non-existing named example.
- User reports incorrect price.
- User reports report felt generic.
- User reports report gave unsupported conclusion.

## 11. Product Risks

| Risk | Mitigation |
|---|---|
| Wrong pin identity | Exact-pin preview, provider comparison, user confirmation before payment. |
| Weak data outside metros | Multi-source fallback, official/open data, public-web gold, clear limitations. |
| Preview feels generic | Use exact pin, use-case lens, and S2 cell location-character profile. |
| Scraped data instability | Per-platform collectors, screenshots/raw artifacts, extraction tests, graceful fallback. |
| Incorrect pricing | Slot-level scrape, unit capture, normalization gate. |
| Report feels generic | Purpose modules, exact-pin visuals, local source signals, no filler. |
| User expects verdict | Clear product language: location understanding, not investment advice. |
| Long wait after payment | Progress page, email delivery, async workflow recovery. |
| Payment/report failure | Idempotent payment handling, retry queue, support/admin tools. |

## 12. Acceptance Criteria

The first production release is acceptable when:

- A user can complete the no-login paid flow end to end.
- The map shows the exact pin before payment.
- The preview is generated quickly and cheaply.
- The preview uses a location-character profile without presenting it as proof.
- Payment starts full report generation.
- The user sees progress.
- The report renders interactively.
- The report link is emailed.
- No report gives a final verdict.
- Every report preserves the exact coordinate.
- Important numbers have source context.
- Public-web gold is collected for relevant use cases.
- Pricing comparisons only appear after normalization.
- Admin can inspect and retry failed report jobs.
