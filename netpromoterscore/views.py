from collections import defaultdict
import datetime
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from .models import PromoterScore
from .forms import PromoterScoreForm
from .decorators import login_required
from .utils import count_score, get_range_name_by_score


class SurveyView(View):

    @method_decorator(login_required)
    def get(self, request):
        return JsonResponse({'survey_is_needed': self.user_needs_survey(request.user)})

    @method_decorator(login_required)
    def post(self, request):
        promoter_score, errors = self.get_promoter_score(request)
        if promoter_score:
            data, status = {'id': promoter_score.pk}, 200
        else:
            data, status = errors, 400
        return JsonResponse(data, status=status)

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
        return not promoter_score or self.time_to_ask(promoter_score) < datetime.datetime.now()

    def get_most_recent_promoter_score(self, user):
        return PromoterScore.objects.filter(user=user).order_by('-created_at').first()

    def time_to_ask(self, promoter_score):
        return promoter_score.created_at.replace(tzinfo=None) + datetime.timedelta(6*365/12)


class NetPromoterScoreView(View):

    @method_decorator(staff_member_required)
    def get(self, request):
        context = self.get_context_data(request)
        return render(request, 'netpromoterscore/base.html', context)

    def get_context_data(self, request):
        rolling = True if request.GET.get('rolling') and int(request.GET.get('rolling')) else False
        period = request.GET.get('period', 'month')
        qs = PromoterScore.objects.group_by_period(period)
        scores = defaultdict(dict)
        for item in qs:
            score, count, period = item['score'], item['count'], item['period']
            user_range = get_range_name_by_score(score)
            scores[period].update( {user_range: count} )
        sort_scores = sorted(scores.iteritems(), key=lambda key_value: key_value[0], reverse=True)
        for _, sc in sort_scores:
            sc['score'] = count_score(sc)
        return {'rolling': rolling, 'scores': sort_scores}