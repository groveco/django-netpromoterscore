import datetime
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME
from promoterscore.models import PromoterScore


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


def get_list_view_context():
    list_of_information =[]
    now = datetime.date.today()
    year = now.year
    month = now.month
    for x in range(0, 11):
        promoter_scores = PromoterScore.objects.filter(created_at__year=year, created_at__month=month)
        list_of_information += (get_information(promoter_scores, month, year),)
        month, year = get_previous_month(month, year)

    return list_of_information


def get_previous_month(month, year):
    month -= 1
    if month == 0:
        year -= 1
        month = 12
    return month, year


def get_information(promoter_scores, month, year):
    date = monthDict[month] + ' ' + str(year)
    promoters = len(promoter_scores.filter(score__in=[10, 9]))
    detractors = len(promoter_scores.filter(score__in=[6, 5, 4, 3, 2, 1]))
    passive = len(promoter_scores.filter(score__in=[7, 8]))
    none = len(promoter_scores.filter(score=None))

    if (promoters + detractors + passive > 0):
        score = get_net_promoter_score(promoters, detractors, passive)
    else:
        score = 'Not enough info.'

    info = {'month': date, 'score': score, 'promoters': promoters, 'detractors': detractors, 'passive': passive, 'none': none }
    return info


def get_net_promoter_score(promoters, detractors, passive):
    total = promoters + detractors + passive
    promoter_percentage = float(promoters) / float(total)
    detractor_percentage = float(detractors) / float(total)
    return round(promoter_percentage - detractor_percentage * 100, 2)
