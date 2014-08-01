from django.db import models
from django.conf import settings


class PromoterScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)
