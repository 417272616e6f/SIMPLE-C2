import app_globals

def get_session_from_request(request):
    """
    Retrieve the session associated with the given request.

    Args:
        request: The incoming request object.

    Returns:
        The session object if found, otherwise None.
    """

    sesid = request.headers.get("x-sesid") or request.headers.get("X-SESID")
    if not sesid:
        return None

    session = app_globals.SESSIONS.get(sesid)
    if session is None:
        return None

    return session
