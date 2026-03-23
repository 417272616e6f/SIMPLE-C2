output.py

Summary
- HTTP POST `/output` endpoint to receive output data from a beacon.
- Parses incoming body (pipe-separated `path|output`) via `functions.output_handler.handle_output`.

Behavior
- Looks up session via header; returns 403 if missing or unknown.
- Records heartbeat, updates session path and output buffer, prints output to local CLI if session is active.
- Returns 201 on success, 500 on error.

Notes
- Uses `prompt_toolkit.print_formatted_text` for safe printing.
