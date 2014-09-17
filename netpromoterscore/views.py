import datetime
import json
import ast
from django.http import HttpResponse
from django.template import Context, loader
from netpromoterscore.models import PromoterScore
from netpromoterscore.app_settings import PROMOTERSCORE_PERMISSION_VIEW
from netpromoterscore.utils import safe_admin_login_prompt


def view_permission(f):
    def wrap(request, *args, **kwargs):
        if not PROMOTERSCORE_PERMISSION_VIEW(request.user):
            return safe_admin_login_prompt(request)
        return f(request, *args, **kwargs)
    return wrap


"""
Creates a Promoter Score for a user
Returns 201 on successful creation
"""

def create_promoter_score(request):
    # TODO add criteria for good request
    score = _get_score(request)
    promoter_score = PromoterScore(user=request.user, score=score)
    promoter_score.save()
    return HttpResponse(
        json.dumps({'score_id': str(promoter_score.pk)}),
        content_type='application/json',
        status=201
    )

def _get_score(request):
    score_raw = ast.literal_eval(request.body)['score']
    return score_raw if score_raw > 0 else None

"""
Check to see if customer should get surveyed
Returns true if customer should get surveyed and false if not
"""

def retrieve_survey(request):
    promoter_score = _get_most_recent_promoter_score(request)
    if _user_needs_survey(promoter_score):
        return HttpResponse(json.dumps({'get_survey': 'true'}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'get_survey': 'false'}), content_type="application/json")

def _get_most_recent_promoter_score(request):
    ps_queryset = PromoterScore.objects.filter(user=request.user)
    return ps_queryset.order_by('created_at').reverse()[0] if ps_queryset else None

def _user_needs_survey(promoter_score):
    return not promoter_score or _time_to_ask(promoter_score) < datetime.datetime.now()


def _time_to_ask(promoter_score):
    return promoter_score.created_at.replace(tzinfo=None) + datetime.timedelta(6*365/12)


"""
Gets the net promoter scores for the net promoter score admin pages
Renders pages on success
"""

@view_permission
def get_net_promoter_score(request):
    rolling = True if request.GET.get('rolling') and int(request.GET.get('rolling')) else False
    t = loader.get_template('netpromoterscore/base.html')
    c = Context({'rolling': rolling, 'nps_info_list': PromoterScore.objects.get_list_view_context(rolling)})
    return HttpResponse(t.render(c))
