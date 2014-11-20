import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from utils import get_next_month


class PromoterScoreManager(models.Manager):
    def rolling(self, month):
        month = get_next_month(month)
        scores = self.filter(created_at__lt=datetime.date(year=month.year, month=month.month, day=1))\
        .order_by('-created_at').values('user', 'score')
        return self._recent_scores(scores)

    def one_month_only(self, month):
        scores = self.filter(created_at__month=month.month, created_at__year=month.year).values('user', 'score')
        return self._recent_scores(scores)

    def _recent_scores(self, scores):
        most_recent_scores = {}
        for score in scores:
            if not score['user'] in most_recent_scores:
                most_recent_scores[score['user']] = score['score']
        return most_recent_scores


class PromoterScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PromoterScoreManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.score = self.score if 1 <= self.score <= 10 else None
        super(PromoterScore, self).save(*args, **kwargs)
