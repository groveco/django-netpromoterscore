from django.test import TestCase
from netpromoterscore.models import PromoterScore
from . import TestMixin

class TestPromoterScoreModels(TestCase, TestMixin):

    def setUp(self):
        self.create_users()
        self.create_promoter_scores()

    def tearDown(self):
        self.delete_promoter_scores()
        self.delete_users()

    def test_rolling_months(self):
        got = PromoterScore.objects.rolling(month=self.now)
        expected = {self.user.pk: self.ps1.score, self.user2.pk: self.ps3.score}
        self.assertEqual(expected, got)

    def test_one_month_only(self):
        got = PromoterScore.objects.one_month_only(month=self.now)
        expected = {self.user.pk: self.ps1.score}
        self.assertEqual(expected, got)
