sessions.py

Summary
- Represents a single beacon session.
- Maintains session id, last heartbeat timestamp, prompt history, last command, path, and output buffer.

API
- `get_id() -> str` : return session id.
- `get_last_heartbeat() -> float` : thread-safe access to last heartbeat time.
- `record_heartbeat() -> Session` : thread-safe update heartbeat timestamp.
- `get_history() -> InMemoryHistory` : returns prompt_toolkit history object.
- `get_total_history() -> list[str]` : total number of history entries.
- `tail_history(n:int=50)` : return last `n` history entries as deque.
- `get_last_command()` / `set_last_command(cmd)` : thread-safe last command storage.
- `get_path()` / `set_path(path)` : thread-safe path storage.
- `append_output(out)` / `tail_output(n=50)` : thread-safe output buffer methods.

Concurrency
- Uses individual `threading.Lock` instances for each mutable attribute to allow safe concurrent access.
