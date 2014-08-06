import datetime
from django.http import HttpResponse
from django.template import Context, loader
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from promoterscore.models import PromoterScore
from promoterscore.app_settings import PROMOTERSCORE_PERMISSION_VIEW
from promoterscore.utils import safe_admin_login_prompt


def view_permission(f):
    def wrap(request, *args, **kwargs):
        if not PROMOTERSCORE_PERMISSION_VIEW(request.user):
            return safe_admin_login_prompt(request)
        return f(request, *args, **kwargs)
    return wrap


class PromoterScoreApiView(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)

    def create(self, request, *args, **kwargs):
        try:
            score_raw = request.DATA.get('score', None)
            # If user does not enter score, set score to less than zero before request
            score = score_raw if score_raw > 0 else None
            created_at = datetime.datetime.now()
            promoter_score = PromoterScore(user=request.user, created_at=created_at, score=score)
            promoter_score.save()
            return HttpResponse("Promoter score successfully taken.")
        except Exception:
            return HttpResponse("UNSUCCESSFUL CREATION OF A PROMOTER SCORE")


class SurveyApiView(viewsets.ViewSet):
    authentication_classes = (SessionAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        ps_queryset = PromoterScore.objects.filter(user=request.user)
        # get the most recent promoter score or None
        self.promoter_score = ps_queryset.order_by('created_at').reverse()[0] if ps_queryset else None

        if not self.promoter_score or self.time_to_ask() < datetime.datetime.now():
            return HttpResponse(content='true', content_type='text/plain')
        else:
            return HttpResponse(content='false', content_type='text/plain')

    def time_to_ask(self):
        return self.promoter_score.created_at.replace(tzinfo=None)+datetime.timedelta(6*365/12)


class NetPromoterScoreView(viewsets.ViewSet):
    @method_decorator(view_permission)
    def dispatch(self, *args, **kwargs):
        return super(NetPromoterScoreView, self).dispatch(*args, **kwargs)

    def get(self, request):
        #context = self.context()
        t = loader.get_template('netpromoterscore/base.html')
#        c = Context({'content': 'This is some content.'})
        c = Context({'nps_info_list': PromoterScore.objects.get_list_view_context()})
        return HttpResponse(t.render(c))
