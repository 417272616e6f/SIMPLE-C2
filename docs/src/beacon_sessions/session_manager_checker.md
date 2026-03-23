session_manager_checker.py

Summary
- Background routine that periodically checks session heartbeats and removes stale sessions.
- Can run either inside an existing asyncio loop or in a dedicated background thread with its own event loop.

Key methods
- `start_check_routine() -> SessionManager` : start the background checking coroutine; supports both current loop or spinning a dedicated loop + thread.
- `stop_check_routine() -> SessionManager` (async) : stop and await cancellation of the background task, tear down background loop and thread if used.
- `is_checking() -> bool` : return whether the check routine is active.

Behavior
- Removes sessions whose last heartbeat is older than 120 seconds.
- Uses `IS_DEBUG` env flag to print lifecycle messages.