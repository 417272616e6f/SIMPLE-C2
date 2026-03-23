import app_globals

from flask import Blueprint, Response, request
from functions.request import get_session_from_request
from functions.encoding import encode_ascii_to_int

bp = Blueprint("command", __name__)

@bp.route("/command", methods=["GET"])
def command():
    """Return the last CLI input as base64-encoded JSON. 204 if none yet."""
    session_finish = False
    try:
        session = get_session_from_request(request)
        if session is None:
            return Response(status=403, mimetype="text/plain; charset=utf-8")

        session.record_heartbeat()
        cmd = session.get_last_command()
        if cmd is None:
            return Response(status=204)

        session_finish = cmd == "exit"
        encoded = encode_ascii_to_int(cmd)
        return Response(encoded, mimetype="text/plain; charset=utf-8")
    finally:
        if session_finish and session is not None:
            session.set_last_command(None)
            app_globals.SESSIONS.remove(session.get_id())