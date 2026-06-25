## What to build
Implement the /appeal endpoint, rate limiting, and the admin-protected audit log view.

## Acceptance criteria
- [ ] `POST /appeal` updates status to "under_review" and logs reasoning.
- [ ] Transparency labels follow the objective/neutral design.
- [ ] `/submit` has rate limiting (10 per min) and returns 429 when exceeded.
- [ ] `GET /log` requires a simulated admin API key in headers.
- [ ] `GET /log` returns structured JSON of all entries.

## Blocked by
- .scratch/provenance-guard/issues/02-multi-signal-scoring.md
