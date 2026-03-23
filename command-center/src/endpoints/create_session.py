import app_globals
from flask import Blueprint, Response, request
from functions.output_handler import handle_output
from beacon_sessions.sessions import Session

bp = Blueprint("whoami", __name__)


@bp.route("/whoami", methods=["POST"])
def whoami():
    """Creates a new session for an incoming beacon and returns the session ID."""
    try:
        session = app_globals.SESSIONS.create_new()
        session.set_path(request.get_data(as_text=True))

        app_globals.SESSIONS.set_active(session.get_id())
        return Response(session.get_id(), status=201, mimetype="text/plain; charset=utf-8")
    except Exception:
        return Response(status=500, mimetype="text/plain; charset=utf-8")
