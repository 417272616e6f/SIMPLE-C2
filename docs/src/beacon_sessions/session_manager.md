session_manager.py

Summary
- Manages in-memory `Session` objects keyed by session id.
- Tracks the currently active session and provides convenience methods.

Key methods
- `set_active(session_id: str) -> SessionManager` : mark a session as active.
- `get_active_session() -> Session | None` : return currently active `Session`.
- `create_new() -> Session` : creates and stores a new `Session` (ids like `b1`, `b2`, ...).
- `values() -> Iterable[Session]` : iterator over stored sessions.
- `get(session_id: str) -> Session` : lookup a session by id.
- `remove(session_id: str) -> SessionManager` : remove a session and adjust active session.

Notes
- Uses `IS_DEBUG` environment flag to print debug info when sessions are removed.
- Does not persist sessions; intended for in-memory beacon connections.
