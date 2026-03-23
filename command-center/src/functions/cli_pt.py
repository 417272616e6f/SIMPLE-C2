import time
import app_globals

from exceptions.force_cli_reload import ForceCLIReload
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import clear as clear_screen

_printed_no_session = False

def run_cli():
    """
    Runs the command-line interface (CLI) for interacting with active sessions.

    The CLI continuously checks for active sessions and allows the user to send commands to them.
    It also supports local commands prefixed with a colon (e.g., :sessions, :history) for managing sessions and viewing command history.
    """

    while True:
        active_session = app_globals.SESSIONS.get_active_session()
        if active_session is None:
            global _printed_no_session
            if not _printed_no_session:
                print_formatted_text("No active sessions. Waiting for beacon whoami...")
                _printed_no_session = True
            time.sleep(0.2)
            continue

        _printed_no_session = False

        sid = active_session._id
        path = active_session.get_path()
        history = active_session.get_history()
        prompt_text = f"({sid}) {path}> " if path else f"({sid})> "
        session = PromptSession(prompt_text, history=history)

        try:
            with patch_stdout():
                line = session.prompt()
        except (EOFError, KeyboardInterrupt) as e:
            print_formatted_text("Exiting CLI.")
            return
        except ForceCLIReload as e:
            print_formatted_text("Reloading CLI...")
            continue
        except Exception as e:
            print_formatted_text(f"Error in CLI: {e}")
            continue

        if not line or not line.strip():
            continue

        # local colon commands
        if line.startswith(":"):
            parts = line[1:].strip().split()
            if not parts:
                print_formatted_text(f"Unknown CLI command: {line}")
                continue

            active_session = app_globals.SESSIONS.get_active_session()
            if active_session is None:
                print_formatted_text("No active session")
                continue

            cmd = parts[0].lower()
            args = parts[1:]

            if cmd == "ss" or cmd == "sessions":
                sub = args[0].lower() if args else "ls"
                if sub == "list" or sub == "ls":
                    for session in app_globals.SESSIONS.values():
                        histlen = session.get_total_history()
                        outlen = len(session._output_buffer)
                        marker = "*" if app_globals.SESSIONS.is_session_active(session._id) else " "
                        print_formatted_text(f"{marker} {session._id} - history:{histlen} output:{outlen}")
                    continue
                else:
                    print_formatted_text(f"Unknown :sessions subcommand: {sub}")
                    continue

            if cmd == "h" or cmd == "history":
                n = int(args[0]) if args else 50

                for i, h in enumerate(active_session.tail_history(n), start=1):
                    print_formatted_text(f"{i}: {h}")
                continue

            if cmd == "s" or cmd == "session":
                if not args:
                    print_formatted_text(f"You must provide a session id to :session")
                    continue

                sid = args[0].lower()
                session_to_activate = app_globals.SESSIONS.get(sid)
                if session_to_activate is None:
                    print_formatted_text(f"Unknown session: {sid}")
                    continue

                app_globals.SESSIONS.set_active(sid)
                session = app_globals.SESSIONS.get_active_session()
                clear_screen()
                for out in session.tail_output(200):
                    print_formatted_text(out)
                continue

            print_formatted_text(f"Unknown CLI command: {line}")
            continue

        active_session = app_globals.SESSIONS.get_active_session()
        if active_session is None:
            print_formatted_text("No active session to send command to.")
            continue

        active_session.set_last_command(line)

        while True:
            active_session = app_globals.SESSIONS.get_active_session()
            if active_session is None:
                continue
            if active_session.get_last_command() is None:
                break
            time.sleep(0.05)
