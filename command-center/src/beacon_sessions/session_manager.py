import os
from typing import Iterable
from .sessions import Session

IS_DEBUG = os.getenv("IS_DEBUG", "").lower() == "true"

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self._active_session_id = None

    def set_active(self, session_id: str) -> "SessionManager":
        if session_id in self.sessions:
            self._active_session_id = session_id
        return self

    def get_active_session(self) -> Session|None:
        if self._active_session_id is None:
            return None
        return self.sessions.get(self._active_session_id)

    def is_session_active(self, session_id: str) -> bool:
        return session_id in self.sessions and self._active_session_id == session_id

    def create_new(self) -> "Session":
        new_id = f"b{len(self.sessions) + 1}"
        new_session = Session(new_id)

        self.sessions[new_session.get_id()] = new_session

        if self._active_session_id is None:
            self._active_session_id = new_session.get_id()

        return new_session

    def values(self) -> Iterable[Session]:
        return self.sessions.values()

    def get(self, session_id: str) -> Session:
        return self.sessions.get(session_id)

    def remove(self, session_id: str) -> "SessionManager":
        if session_id not in self.sessions:
            return self

        del self.sessions[session_id]
        if IS_DEBUG:
            print(f"Session {session_id} removed due to inactivity.")

        if self._active_session_id == session_id:
            self._active_session_id = next(iter(self.sessions), None)
            if IS_DEBUG:
                print(f"Active session removed. New active session: {self._active_session_id}")

        return self