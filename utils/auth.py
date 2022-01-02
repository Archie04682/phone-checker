import base64
import os
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()


class AppUser(UserMixin):
    pass


app_key = os.environ.get("MOBILE_API_KEY", "dummy-api-key")


def _get_user_by_api_key(key: str):
    if key == app_key:
        return AppUser()
    return None


@login_manager.request_loader
def load_user_from_request(req):
    api_key = req.args.get('api_key')
    if api_key:
        user = _get_user_by_api_key(api_key)
        if user:
            return user

    api_key = req.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = _get_user_by_api_key(api_key)
        if user:
            return user

    return None


def init_app_auth(app):
    login_manager.init_app(app)
