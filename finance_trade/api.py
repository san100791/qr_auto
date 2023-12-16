from flask import Flask, request, g

from finance_trade.config import init_sentry_flask
from finance_trade.error_handlers.auth_error_handler import custom_error_handler
from finance_trade.exceptions import CustomException
from finance_trade.services import core
from finance_trade.services.auth_service import AuthService
from finance_trade.auth_controller.view import user_bp


def auth_handler():
    _as = AuthService()
    user_id = _as.auth(request)
    g.user_id = user_id

def teardown_request_handler():
    g.user_id = None


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config["JSON_SORT_KEYS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.url_map.strict_slashes = False

    # TODO: add sentry dsn
    # init_sentry_flask(sentry_conf=core.config.sentry, environment=core.config.env)

    app.before_request(auth_handler())
    app.after_request(teardown_request_handler())
    app.errorhandler(CustomException, custom_error_handler)

    app.register_blueprint(user_bp, url_prefix="/api/v1/user")
    return app

app = create_app()

@app.route("/healthcheck")
def healthcheck():
    """Endpoint show work api or die
    ---
    get:
        description: live or die
        tags:
            - Application
        responses:
            200:
                description: live or die
    """
    return "", 200


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
