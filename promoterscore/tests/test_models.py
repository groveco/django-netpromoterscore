import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from promoterscore.models import PromoterScore


class TestPromoterScoreModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='jared', email='jared@hotmail.com', password='foobar123')
        self.user1.save()
        self.user2 = User.objects.create_user(username='cole', email='cole@hotmail.com', password='foobar321')
        self.now = datetime.datetime.now()
        self.ps1 = PromoterScore(user=self.user1, score=8)
        self.ps1.save()
        self.ps2 = PromoterScore(user=self.user1, score=9)
        self.ps2.save()
        self.ps2.created_at = self.now+datetime.timedelta(-4*365/12)
        self.ps2.save()
        self.ps3 = PromoterScore(user=self.user2, score=9)
        self.ps3.save()
        self.ps3.created_at = self.now+datetime.timedelta(-7*365/12)
        self.ps3.save()

    def test_rolling_months(self):
        got = PromoterScore.objects._rolling(month=self.now)
        expected = {self.user1.pk: self.ps1.score, self.user2.pk: self.ps3.score}
        self.assertEqual(expected, got)

    def test_one_month_only(self):
        got = PromoterScore.objects._one_month_only(month=self.now)
        expected = {self.user1.pk: self.ps1.score}
        self.assertEqual(expected, got)
