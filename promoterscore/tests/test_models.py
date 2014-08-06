import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from promoterscore.models import PromoterScore


class TestPromoterScoreModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='jared', email='jared@hotmail.com', password='foobar123')
        self.user1.save()
        self.user2 = User.objects.create_user(username='cole', email='cole@hotmail.com', password='foobar321')

    def test_rolling_months(self):
        now = datetime.datetime.now()
        ps1 = PromoterScore(user=self.user1, score=8)
        ps1.save()
        ps2 = PromoterScore(user=self.user1, score=9)
        ps2.save()
        ps2.created_at = now+datetime.timedelta(-4*365/12)
        ps2.save()
        ps3 = PromoterScore(user=self.user2, score=9)
        ps3.save()
        ps3.created_at = now+datetime.timedelta(-7*365/12)
        ps3.save()
        got = PromoterScore.objects._rolling(month=now)
        expected = {self.user1.pk: ps1.score, self.user2.pk: ps3.score}
        self.assertEqual(expected, got)