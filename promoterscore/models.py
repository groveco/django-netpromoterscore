from django.db import models
from django.conf import settings
from utils import monthDict, get_many_previous_months
import datetime


class PromoterScoreManager(models.Manager):

    def get_list_view_context(self):
        now = datetime.date.today().replace(day=1)

        months = [now] + get_many_previous_months(now)
        scores_by_month = [self._get_netpromoter(month) for month in months]
        return scores_by_month

    def promoters(self, month):
        return len(self.filter(created_at__month=month.month, created_at__year=month.year, score__in=[10, 9]))

    def detractors(self, month):
        return len(self.filter(created_at__month=month.month, created_at__year=month.year, score__in=[6, 5, 4, 3, 2, 1]))

    def passive(self, month):
        return len(self.filter(created_at__month=month.month, created_at__year=month.year, score__in=[8, 7]))

    def skipped(self, month):
        return len(self.filter(created_at__month=month.month, created_at__year=month.year, score=None))

    def _rolling(self, month):
        most_recent_scores = {}
        scores = self.filter(created_at__lt=datetime.date(year=month.year, month=month.month+1, day=1)).order_by('-created_at').values('user', 'score')
        for score in scores:
            if not score['user'] in most_recent_scores:
                most_recent_scores[score['user']] = score['score']
        return most_recent_scores

    def _get_netpromoter(self, month, rolling=False):
        label = monthDict[month.month] + ' ' + str(month.year)
        return NetPromoterScore(label, self.promoters(month), self.detractors(month), self.passive(month), self.skipped(month))



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
