from dotenv import load_dotenv
load_dotenv()

import logging
from flask import Flask
from beacon_sessions.session_manager import SessionManager
from beacon_sessions.session_manager_checker import SessionManagerChecker

SERVER = Flask(__name__)
SESSIONS = SessionManager()
SESSIONS_CHECKER = SessionManagerChecker(SESSIONS)

log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

# Silence Flask/werkzeug logs and the CLI server banner so no Flask output appears.
try:
    logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
    logging.getLogger('werkzeug').propagate = False
    logging.getLogger('flask').setLevel(logging.CRITICAL)
    logging.getLogger('flask').propagate = False
    import flask.cli as _flask_cli
    _flask_cli.show_server_banner = lambda *a, **k: None
except Exception:
    pass