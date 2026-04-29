# LocationIQ

LocationIQ is a no-login, paid location intelligence report product for Indian users evaluating a real-world location decision.

The first build follows the contracts in:

- [technical-spec.md](/Users/sailsabnis/Insig8/LocationIQ-New/technical-spec.md)
- [docs/product-requirements.md](/Users/sailsabnis/Insig8/LocationIQ-New/docs/product-requirements.md)
- [docs/api-data-model-spec.md](/Users/sailsabnis/Insig8/LocationIQ-New/docs/api-data-model-spec.md)
- [docs/ux-report-ui-spec.md](/Users/sailsabnis/Insig8/LocationIQ-New/docs/ux-report-ui-spec.md)

## Repository Layout

```text
apps/web                 Next.js customer experience
services/api             FastAPI lifecycle API
infra/supabase           Supabase/PostGIS migrations
packages/report-schema   Local package wrapper for report schema
packages/taxonomy        Local package wrapper for input taxonomy
docs                     Product/API/UX planning docs
report-templates         Canonical report contracts
sample-reports           Historical and current HTML report prototypes
```

## Local Development

Install JavaScript dependencies:

```bash
npm install
```

Install API dependencies:

```bash
cd services/api
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run the API:

```bash
npm run dev:api
```

Run the web app:

```bash
npm run dev:web
```

The current implementation uses mock provider adapters for location resolution, S2 cell profiling, checkout, and report generation. This lets the no-login product flow run before paid provider keys are configured.

## Provider Configuration

The API loads `.env.local` from the repository root.

Payment:

- `LOCATIONIQ_PAYMENT_PROVIDER=mock` keeps local checkout mocked.
- If `RAZORPAY_KEY_ID` or `NEXT_PUBLIC_RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` are set, the API can create Razorpay orders.
- `RAZORPAY_WEBHOOK_SECRET` is required before enabling real Razorpay webhook verification.

Storage:

- `LOCATIONIQ_STORAGE=memory` uses local in-memory records.
- `LOCATIONIQ_STORAGE=supabase` uses `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` from server-side API code.
- `npm run check:supabase` checks whether the required Supabase tables are reachable after migration.
- LocationIQ stores exact pins in `report_locations` to avoid colliding with existing generic `locations` tables.

Do not expose `SUPABASE_SERVICE_ROLE_KEY`, `RAZORPAY_KEY_SECRET`, or provider server keys to the browser.
