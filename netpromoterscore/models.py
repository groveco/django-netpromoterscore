from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models import Count


class PromoterScoreManager(models.Manager):

    def group_by_period(self, period, rolling=False):
        select = {'period': "date_trunc('%s', created_at)" % period}
        return self.extra(select=select, order_by=['score', 'period']).values('score', 'period').annotate(count=Count('score'))


class PromoterScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    reason = models.TextField(null=True, blank=True)

    objects = PromoterScoreManager()