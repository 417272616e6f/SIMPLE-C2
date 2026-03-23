import app_globals
from flask import Blueprint, Response, request
from functions.output_handler import handle_output
from functions.request import get_session_from_request
from prompt_toolkit import print_formatted_text

bp = Blueprint("output", __name__)

@bp.route("/output", methods=["POST"])
def output():
    """Receive output data from agents and associate it with the correct session. """
    try:
        session = get_session_from_request(request)
        if session is None:
            return Response(status=403, mimetype="text/plain; charset=utf-8")

        session.record_heartbeat()

        body = request.get_data(as_text=True)
        parsed = handle_output(body)

        path = parsed.get("path") if isinstance(parsed, dict) else ""
        out = parsed.get("output") if isinstance(parsed, dict) else parsed

        session.set_path(path)
        session.append_output(out)

        if app_globals.SESSIONS.is_session_active(session.get_id()):
            print_formatted_text(out)

        session.set_last_command(None)
        return Response(status=201, mimetype="text/plain; charset=utf-8")
    except Exception:
        return Response(status=500, mimetype="text/plain; charset=utf-8")