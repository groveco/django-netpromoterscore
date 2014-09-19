import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from .models import PromoterScore
from .forms import PromoterScoreForm
from .decorators import login_required, admin_required
from .utils import get_many_previous_months, monthDict, count_score


CHECKS = {
    'promoters': lambda x: 9 <= x <= 10,
    'detractors': lambda x: 1 <= x <= 6,
    'passive': lambda x: 7 <= x <= 8,
    'skipped': lambda x: x is None
}


class SurveyView(View):

    @method_decorator(login_required)
    def get(self, request):
        data = {'survey_is_needed': True if self.user_needs_survey(request.user) else False}
        return HttpResponse(json.dumps(data), content_type="application/json")

    @method_decorator(login_required)
    def post(self, request):
        promoter_score, errors = self.get_promoter_score(request)
        if promoter_score:
            data, status = {'id': promoter_score.pk}, 200
        else:
            data, status = errors, 400
        return HttpResponse(json.dumps(data), content_type='application/json', status=status)

    def get_promoter_score(self, request):
        data = json.loads(request.body)
        data['user'] = request.user.id
        pk = data.pop('id', None)

        if pk:
            instance = get_object_or_404(PromoterScore, pk=pk)
        else:
            instance = None

        form = PromoterScoreForm(data, instance=instance)

        return form.save() if form.is_valid() else None, form.errors

    def user_needs_survey(self, user):
        promoter_score = self.get_most_recent_promoter_score(user)
        if promoter_score:
            print promoter_score.created_at, self.time_to_ask(promoter_score), datetime.datetime.now()
        return not promoter_score or self.time_to_ask(promoter_score) < datetime.datetime.now()

    def get_most_recent_promoter_score(self, user):
        return PromoterScore.objects.filter(user=user).order_by('-created_at').first()

    def time_to_ask(self, promoter_score):
        return promoter_score.created_at.replace(tzinfo=None) + datetime.timedelta(6*365/12)


class NetPromoterScoreView(View):

    @method_decorator(admin_required)
    def get(self, request):
        context = self.get_context_data(request)
        return render(request, 'netpromoterscore/base.html', context)

    def get_context_data(self, request):
        rolling = True if request.GET.get('rolling') and int(request.GET.get('rolling')) else False
        return {'rolling': rolling, 'nps_info_list': self.get_list_view_context(rolling)}

    def get_list_view_context(self, rolling):
        now = datetime.date.today().replace(day=1)

        months = [now] + get_many_previous_months(now)
        scores_by_month = [self.get_netpromoter(month, rolling) for month in months]
        return scores_by_month

    def get_netpromoter(self, month, rolling):
        label = monthDict[month.month] + ' ' + str(month.year)
        if rolling:
            scores = PromoterScore.objects.rolling(month)
        else:
            scores = PromoterScore.objects.one_month_only(month)

        result = {}
        for name, check in CHECKS.items():
            result[name] = self.sum(scores, check)
        result['score'] = count_score(**result)
        result['label'] = label

        return result

    def sum(self, scores, check):
        return sum([1 for score in scores.values() if check(score)])