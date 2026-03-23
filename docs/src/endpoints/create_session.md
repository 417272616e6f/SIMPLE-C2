create_session.py

Summary
- HTTP POST `/whoami` endpoint to create a new session.

Behavior
- Creates a new `Session` via `app_globals.SESSIONS.create_new()`.
- Sets the session path from the POST body (`request.get_data(as_text=True)`), marks the session active, and returns the session id with 201 status.
- Returns 500 on unexpected errors.

Notes
- Intended to be called by a beacon client when it starts, providing its current path in the request body.
