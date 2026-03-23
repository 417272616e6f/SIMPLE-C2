app_globals.py

Summary
- Central module that initializes the Flask `SERVER`, session manager, and session checker.
- Silences Flask/werkzeug logging and server banner for a clean CLI experience.

Exports
- `SERVER` : Flask application instance used to register blueprints.
- `SESSIONS` : `SessionManager` singleton for tracking beacon sessions.
- `SESSIONS_CHECKER` : `SessionManagerChecker` instance that monitors session heartbeats.
- `log` : logger instance used to adjust log levels.

Notes
- Calls `load_dotenv()` at import time to load environment variables.
- Sets `werkzeug` and `flask` loggers to `CRITICAL` and disables propagation.
- Intended to be imported by other modules to access global singletons.
