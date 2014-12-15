from django.http import HttpResponse


def login_required(f):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponse(status=401)
        return f(request, *args, **kwargs)
    return wrap