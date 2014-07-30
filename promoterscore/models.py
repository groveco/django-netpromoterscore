from django.db import models
from django.conf import settings


class PromoterScore(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL)
    taken_at = models.DateTimeField()
    score = models.IntegerField(null=True, blank=True)
