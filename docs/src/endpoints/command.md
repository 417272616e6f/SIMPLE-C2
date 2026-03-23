command.py

Summary
- HTTP GET `/command` endpoint that returns the last CLI input for a session.
- Encodes the last command as ASCII integer sequence (space-separated) using `functions.encoding.encode_ascii_to_int`.

Behavior
- Reads session id from `x-sesid` header via `get_session_from_request`.
- Returns 403 if session not found, 204 if no pending command, or the encoded command as plain text.
- If the command equals `exit`, clears the last_command and removes the session.

Notes
- Designed for beacon clients to poll for commands.
