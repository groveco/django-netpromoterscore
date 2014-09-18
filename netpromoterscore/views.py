import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .models import PromoterScore
from .forms import PromoterScoreForm


class SurveyView(View):

    def get(self, request):
        data = {'survey_is_needed': True if self._user_needs_survey(request.user) else False}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def post(self, request):
        promoter_score, errors = self._get_promoter_score(request)
        if promoter_score:
            data, status = {'id': promoter_score.pk}, 200
        else:
            data, status = errors, 400
        return HttpResponse(json.dumps(data), content_type='application/json', status=status)

    def _get_promoter_score(self, request):
        data = json.loads(request.body)
        data['user'] = request.user.id
        pk = data.pop('id', None)

        if pk:
            instance = get_object_or_404(PromoterScore, pk=pk)
        else:
            instance = None

        form = PromoterScoreForm(data, instance=instance)

        return form.save() if form.is_valid() else None, form.errors

    def _user_needs_survey(self, user):
        promoter_score = self._get_most_recent_promoter_score(user)
        if promoter_score:
            print promoter_score.created_at, self._time_to_ask(promoter_score), datetime.datetime.now()
        return not promoter_score or self._time_to_ask(promoter_score) < datetime.datetime.now()

    def _get_most_recent_promoter_score(self, user):
        return PromoterScore.objects.filter(user=user).order_by('-created_at').first()

    def _time_to_ask(self, promoter_score):
        return promoter_score.created_at.replace(tzinfo=None) + datetime.timedelta(6*365/12)


class NetPromoterScoreView(View):

    def get(self, request):
        rolling = True if request.GET.get('rolling') and int(request.GET.get('rolling')) else False
        context = {'rolling': rolling, 'nps_info_list': PromoterScore.objects.get_list_view_context(rolling)}
        return render(request, 'netpromoterscore/base.html', context)
