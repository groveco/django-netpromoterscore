from django.db import models
from django.conf import settings
from utils import monthDict, get_many_previous_months, get_next_month
import datetime


class PromoterScoreManager(models.Manager):

    def get_list_view_context(self, rolling):
        now = datetime.date.today().replace(day=1)

        months = [now] + get_many_previous_months(now)
        scores_by_month = [self._get_netpromoter(month, rolling) for month in months]
        return scores_by_month

    def promoters(self, scores):
        total_promoters = 0
        for score in scores.values():
            if 9 <= score <= 10:
                total_promoters += 1
        return total_promoters

    def detractors(self, scores):
        total_detractors = 0
        for score in scores.values():
            if 1 <= score <= 6:
                total_detractors += 1
        return total_detractors

    def passive(self, scores):
        total_passive = 0
        for score in scores.values():
            if 7 <= score <= 8:
                total_passive += 1
        return total_passive

    def skipped(self, scores):
        total_skipped = 0
        for score in scores.values():
            if score is None:
                total_skipped += 1
        return total_skipped

    def _rolling(self, month):
        most_recent_scores = {}
        month = get_next_month(month)
        scores = self.filter(created_at__lt=datetime.date(year=month.year, month=month.month, day=1)).order_by('-created_at').values('user', 'score')
        for score in scores:
            if not score['user'] in most_recent_scores:
                most_recent_scores[score['user']] = score['score']
        return most_recent_scores

    def _one_month_only(self, month):
        months_scores = {}
        scores = self.filter(created_at__month=month.month, created_at__year=month.year).values('user', 'score')
        for score in scores:
            if not score['user'] in months_scores:
                months_scores[score['user']] = score['score']
        return months_scores

    def _get_netpromoter(self, month, rolling):
        label = monthDict[month.month] + ' ' + str(month.year)
        scores = self._rolling(month) if rolling is True else self._one_month_only(month)
        return NetPromoterScore(label, self.promoters(scores), self.detractors(scores), self.passive(scores), self.skipped(scores))


class NetPromoterScore(object):

    def __init__(self, label, promoters, detractors, passive, skipped):
        self.label = label
        self.promoters = promoters
        self.detractors = detractors
        self.passive = passive
        self.skipped = skipped

    @property
    def score(self):
        total = self.promoters + self.detractors + self.passive
        if total > 0:
            promoter_percentage = float(self.promoters) / float(total)
            detractor_percentage = float(self.detractors) / float(total)
            return round(promoter_percentage - detractor_percentage * 100, 2)
        else:
            return 'Not enough information.'


class PromoterScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)

    objects = PromoterScoreManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.score = self.score if 1 <= self.score <= 10 else None
        super(PromoterScore, self).save(*args, **kwargs)
