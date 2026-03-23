request.py

Summary
- Helper to resolve a `Session` from an incoming Flask request.

API
- `get_session_from_request(request) -> Session | None` : reads `x-sesid` (case-insensitive) header and returns the matching session or `None`.

Notes
- Returns `None` if header missing or session id unknown.
- Used by endpoints to enforce session-scoped behavior (e.g., `/command`, `/output`).
