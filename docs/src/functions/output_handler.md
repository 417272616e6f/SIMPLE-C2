output_handler.py

Summary
- Parses output payloads received from beacons.

API
- `handle_output(response: str) -> dict` : Accepts a string and returns a dict with keys `path` and `output`.

Behavior
- If input is not a string, returns `{"path": "", "output": response}`.
- If the string doesnt contains `|`, returns the whole string as `output` and the `path` empty.
- If the string contains `|`, splits on the first `|` and returns the first part as `path` and the second part as `output` in a dict like `{"path": path, "output": output}`.
