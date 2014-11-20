import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from utils import get_next_month


class PromoterScoreManager(models.Manager):
    def rolling(self, month):
        month = get_next_month(month)
        scores = self.filter(created_at__lt=month).order_by('-created_at').values_list('user', 'score')
        return dict(scores)

    def one_month_only(self, month):
        scores = self.filter(created_at__month=month.month, created_at__year=month.year).values_list('user', 'score')
        return dict(scores)


class PromoterScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PromoterScoreManager()