from django.http import HttpResponse
from .app_settings import PROMOTERSCORE_PERMISSION_VIEW
from .utils import safe_admin_login_prompt


def login_required(f):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponse(status=401)
        return f(request, *args, **kwargs)
    return wrap


def admin_required(f):
    def wrap(request, *args, **kwargs):
        if not PROMOTERSCORE_PERMISSION_VIEW(request.user):
            return safe_admin_login_prompt(request)
        return f(request, *args, **kwargs)
    return wrap
