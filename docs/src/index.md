index.py

Summary
- CLI entrypoint when running the server directly (`python index.py`).
- Registers API blueprints and starts the background CLI thread and Flask server.

Behavior
- Reads `IS_DEBUG` from env to decide debug behavior.
- Calls `SESSIONS_CHECKER.start_check_routine()` to ensure session cleanup runs. _(needs more work)_
- Launches `run_cli()` in a daemon thread and then starts the Flask `SERVER` on port 443.

Usage
- Run directly to start the service and local CLI.
