from flask import Request, abort, g, request, flash, redirect, Flask
from flask_login import LoginManager, user_loaded_from_header, login_url

from . import token_manager
from ..controllers.api.response import bad_request, unauthorized
from ..models import User

login_manager = LoginManager()
login_manager.login_view = "login.login"
login_manager.login_message_category = "danger"
login_manager.needs_refresh_message_category = "danger"


@login_manager.request_loader
def load_user_from_header(r: Request):
    authorization_value = r.headers.get('Authorization')
    if not authorization_value:
        return None

    scheme, token = authorization_value.split(' ', 1)

    if scheme != 'Bearer':
        abort(400, bad_request('Malformed authorization'))

    return token_manager.load_user(token)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    if request.path.startswith("/api"):
        return unauthorized()
    else:
        flash(login_manager.login_message, category='danger')
        return redirect(login_url(login_manager.login_view, request.url))


@user_loaded_from_header.connect
def on_user_loaded_from_header(*_):
    g.login_via_header = True


def init_app(app: Flask):
    login_manager.init_app(app)