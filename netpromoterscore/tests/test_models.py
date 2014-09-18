import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from netpromoterscore.models import PromoterScore, NetPromoterScore


class TestPromoterScoreModels(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

        self.user1 = self.user_model.objects.create_user(
            username='jared', email='jared@hotmail.com', password='foobar123'
        )
        self.user2 = self.user_model.objects.create_user(
            username='cole', email='cole@hotmail.com', password='foobar321'
        )

        self.now = datetime.datetime.now()

        self.ps1 = PromoterScore(user=self.user1, score=8)
        self.ps1.save()
        self.ps2 = PromoterScore(user=self.user1, score=9)
        self.ps2.save()
        self.ps2.created_at = self.now - datetime.timedelta(4*365/12)
        self.ps2.save()
        self.ps3 = PromoterScore(user=self.user2, score=9)
        self.ps3.save()
        self.ps3.created_at = self.now - datetime.timedelta(7*365/12)
        self.ps3.save()

    def test_rolling_months(self):
        got = PromoterScore.objects._rolling(month=self.now)
        expected = {self.user1.pk: self.ps1.score, self.user2.pk: self.ps3.score}
        self.assertEqual(expected, got)

    def test_one_month_only(self):
        got = PromoterScore.objects._one_month_only(month=self.now)
        expected = {self.user1.pk: self.ps1.score}
        self.assertEqual(expected, got)

    def test_get_netpromoter_with_rolling(self):
        got = PromoterScore.objects._get_netpromoter(month=self.now, rolling=True)
        self.assertEqual([1, 1], [got.promoters, got.passive])

    def test_get_netpromoter_without_rolling(self):
        got = PromoterScore.objects._get_netpromoter(month=self.now, rolling=False)
        self.assertEqual([0, 1], [got.promoters, got.passive])

class TestNetPromoterScoreModels(TestCase):

    def test_net_promoter_score_calculation(self):
        self.label = 'January 2014'
        self.promoters = 50
        self.detractors = 25
        self.passive = 25
        self.skipped = 0
        nps = NetPromoterScore(self.label, self.promoters, self.detractors, self.passive, self.skipped)
        self.assertEqual(float(25.0), nps.score)
