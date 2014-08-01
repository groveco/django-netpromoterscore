from django.db import models
from django.conf import settings


class PromoterScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.score = self.score if 1 <= self.score <= 10 else None
        super(PromoterScore, self).save(*args, **kwargs)
