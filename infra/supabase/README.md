# Supabase

The initial migration creates the LocationIQ lifecycle, exact-pin, source-run, public-web, pricing, visual, report, and S2/location-character tables described in the API/data model spec.

Run it with the Supabase CLI once a local or hosted project is configured:

```bash
supabase db push
```

Customer-facing traffic should not use direct Supabase table access. The public web app talks to the FastAPI service, and the API uses server-side credentials for persistence.
