import os
import threading
import app_globals

from functions.cli_pt import run_cli

# register blueprints
from endpoints.command import bp as command_bp
from endpoints.output import bp as output_bp
from endpoints.create_session import bp as create_session_bp

app_globals.SERVER.register_blueprint(command_bp)
app_globals.SERVER.register_blueprint(output_bp)
app_globals.SERVER.register_blueprint(create_session_bp)

if __name__ == "__main__":
    IS_DEBUG = os.getenv("IS_DEBUG", "").lower() == "true"
    app_globals.SESSIONS_CHECKER.start_check_routine()


    cli_thread = threading.Thread(target=run_cli, daemon=True)
    cli_thread.start()
    app_globals.SERVER.run(host="0.0.0.0", port=443, threaded=True, use_reloader=False)