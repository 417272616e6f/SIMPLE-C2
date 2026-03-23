import threading
from time import time as utime
from collections import deque
from prompt_toolkit.history import InMemoryHistory

class Session:
    def __init__(self, session_id: str):
        self._id = session_id
        self._last_heartbeat = utime()
        self._history = InMemoryHistory()
        self._last_command = None
        self._path = ""
        self._output_buffer = []

        self._last_heartbeat_lock = threading.Lock()
        self._path_lock = threading.Lock()
        self._last_command_lock = threading.Lock()
        self._output_buffer_lock = threading.Lock()

    def get_id(self) -> str:
        return self._id

    def get_last_heartbeat(self) -> float:
        with self._last_heartbeat_lock:
            return self._last_heartbeat

    def record_heartbeat(self) -> "Session":
        with self._last_heartbeat_lock:
            self._last_heartbeat = utime()
        return self

    def get_history(self) -> InMemoryHistory:
        return self._history

    def get_total_history(self) -> list[str]:
        return sum(1 for _ in self._history.get_strings())

    def tail_history(self, n: int = 50):
        return deque(self._history.get_strings(), maxlen=n)

    def get_last_command(self) -> str|None:
        with self._last_command_lock:
            return self._last_command

    def set_last_command(self, cmd: str|None) -> "Session":
        with self._last_command_lock:
            self._last_command = cmd
        return self

    def get_path(self) -> str:
        with self._path_lock:
            return self._path

    def set_path(self, path: str) -> "Session":
        with self._path_lock:
            if not isinstance(path, str):
                path = ""

            self._path = path
            return self

    def append_output(self, out: str) -> "Session":
        with self._output_buffer_lock:
            self._output_buffer.append(out)
        return self

    def tail_output(self, n: int = 50):
        with self._output_buffer_lock:
            return self._output_buffer[-n:]