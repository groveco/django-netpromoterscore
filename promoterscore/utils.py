import datetime
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME


monthDict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
             9: 'September', 10: 'October', 11: 'November', 12: 'December'}


def safe_admin_login_prompt(request):
    defaults = {
        'template_name': 'admin/login.html',
        'authentication_form': AdminAuthenticationForm,
        'extra_context': {
            'title': 'Log in',
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        },
    }
    return login(request, **defaults)


def get_many_previous_months(month, total_months=12):
    months = []
    for x in xrange(total_months):
        month = _get_previous_month(month)
        months.append(month)
    return months

def _get_previous_month(date):
    month = date.month - 1
    if month == 0:
        return datetime.date(year=date.year-1, month=12, day=1)
    return datetime.date(year=date.year, month=month, day=1)
