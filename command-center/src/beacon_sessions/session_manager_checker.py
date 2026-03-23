import os
import asyncio
import threading

from time import time as utime
from .session_manager import SessionManager

IS_DEBUG = os.getenv("IS_DEBUG", "").lower() == "true"

class SessionManagerChecker:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self._check_sessions_task = None
        self._bg_loop = None
        self._bg_thread = None

    async def _check_sessions(self):
        current_time = utime()
        for session in self.session_manager.values():
            delta = current_time - session.get_last_heartbeat()

            if delta > 120:
                self.session_manager.remove(session.get_id())

    async def _start_check_sessions_routine(self):
        if IS_DEBUG:
            print("Starting session check routine...")

        while True:
            await self._check_sessions()
            await asyncio.sleep(1)

    def start_check_routine(self) -> "SessionManager":
        """Start the background session-checking coroutine.

        Must be called from within a running asyncio event loop.
        """
        if self._check_sessions_task is not None and not getattr(self._check_sessions_task, "done", lambda: False)():
            return self

        # If an asyncio loop is already running in this thread, schedule the task there.
        try:
            loop = asyncio.get_running_loop()
            self._check_sessions_task = loop.create_task(self._start_check_sessions_routine())
            return self
        except RuntimeError:
            pass

        # Otherwise, create a dedicated background thread with its own event loop.
        def _run_loop(loop: asyncio.AbstractEventLoop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        loop = asyncio.new_event_loop()
        t = threading.Thread(target=_run_loop, args=(loop,), daemon=True)
        t.start()

        future = asyncio.run_coroutine_threadsafe(self._start_check_sessions_routine(), loop)
        self._check_sessions_task = future
        self._bg_loop = loop
        self._bg_thread = t
        return self

    async def stop_check_routine(self) -> "SessionManager":
        """Cancel and await the background session-checking coroutine."""
        if self._check_sessions_task is None:
            return self

        task = self._check_sessions_task

        # If this is an asyncio.Task running in the current loop
        if isinstance(task, asyncio.Task):
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        else:
            # Assume a concurrent.futures.Future from run_coroutine_threadsafe
            try:
                task.cancel()
            except Exception:
                pass
            try:
                # attempt to fetch result to let it finish
                task.result(timeout=1)
            except Exception:
                pass

            # stop background loop and join thread
            if self._bg_loop is not None:
                try:
                    self._bg_loop.call_soon_threadsafe(self._bg_loop.stop)
                except Exception:
                    pass
            if self._bg_thread is not None:
                try:
                    self._bg_thread.join(timeout=1)
                except Exception:
                    pass

            self._bg_loop = None
            self._bg_thread = None

        self._check_sessions_task = None
        if IS_DEBUG:
            print("Session check routine stopped.")
        return self

    def is_checking(self) -> bool:
        """Return True if the background check routine is running."""
        return self._check_sessions_task is not None and not self._check_sessions_task.done()