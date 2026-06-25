## What to build
Set up the Flask application, SQLite database, and the first "Tracer Bullet" path: `POST /submit` -> Groq LLM Signal -> SQLite Audit Log.

## Acceptance criteria
- [ ] Flask app runs on port 5000.
- [ ] SQLite database is initialized with `audit_log` table.
- [ ] `POST /submit` accepts JSON with `text` and `creator_id`.
- [ ] System calls Groq API for the first signal.
- [ ] Result is logged to SQLite with a `content_id`.
- [ ] Endpoint returns JSON with `content_id`, `attribution`, `confidence`, and `label`.

## Blocked by
None - can start immediately
