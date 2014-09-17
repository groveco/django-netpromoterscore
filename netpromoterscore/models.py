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
        return self.segment(scores, lambda x: 9 <= x <= 10)

    def detractors(self, scores):
        return self.segment(scores, lambda x: 1 <= x <= 6)

    def passive(self, scores):
        return self.segment(scores, lambda x: 7 <= x <= 8)

    def skipped(self, scores):
        return self.segment(scores, lambda x: x is None)

    def segment(self, scores, test):
        return sum([test(score) for score in scores.values()])

    def _rolling(self, month):
        month = get_next_month(month)
        scores = self.filter(created_at__lt=datetime.date(year=month.year, month=month.month, day=1)).order_by('-created_at').values('user', 'score')
        return self.recent_scores(scores)

    def _one_month_only(self, month):
        scores = self.filter(created_at__month=month.month, created_at__year=month.year).values('user', 'score')
        return self.recent_scores(scores)

    def recent_scores(self, scores):
        most_recent_scores = {}
        for score in scores:
            if not score['user'] in most_recent_scores:
                most_recent_scores[score['user']] = score['score']
        return most_recent_scores

    def _get_netpromoter(self, month, rolling):
        label = monthDict[month.month] + ' ' + str(month.year)
        scores = self._rolling(month) if rolling else self._one_month_only(month)
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
            return round((promoter_percentage - detractor_percentage) * 100, 2)
        else:
            return 'Not enough information.'


class PromoterScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    objects = PromoterScoreManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.score = self.score if 1 <= self.score <= 10 else None
        super(PromoterScore, self).save(*args, **kwargs)
