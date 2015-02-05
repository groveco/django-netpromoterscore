from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, connection
from django.conf import settings
from netpromoterscore.app_settings import PROMOTERSCORE_USER_RANGES


class PromoterScoreManager(models.Manager):

    def group_by_period(self, period):
        ranges = ' UNION ALL '.join(
            [
            'SELECT %s minRange, %s maxRange, \'%s\' "range"' % (values[0], values[-1], range)
            for range, values in PROMOTERSCORE_USER_RANGES.iteritems()
            ]
        )
        query = '''
                    SELECT date_trunc('{0}', created_at), ranges."range", count(nps.score) as "number of occurences"
                    FROM ({1}) as ranges
                    LEFT JOIN netpromoterscore_promoterscore AS nps ON score BETWEEN ranges.minRange AND ranges.maxRange
                    GROUP BY
                        ranges.range,
                        date_trunc('{0}', created_at)
                    ORDER BY
                        date_trunc('{0}', created_at)
                '''\
        .format(period, ranges)

        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()



class PromoterScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=-1, validators=[MinValueValidator(-1), MaxValueValidator(10)])
    reason = models.TextField(null=True, blank=True)

    objects = PromoterScoreManager()