import datetime
from django.test import TestCase
from netpromoterscore.utils import get_many_previous_months, get_next_month, count_score


class TestUtils(TestCase):

    def test_get_many_previous_months(self):
        start_month = datetime.date(year=2014, month=2, day=21)
        got = get_many_previous_months(month=start_month, total_months=3)
        expected = [datetime.date(year=2014, month=1, day=1), datetime.date(year=2013, month=12, day=1), datetime.date(year=2013, month=11, day=1)]
        self.assertEqual(expected, got)

    def test_get_next_month(self):
        start_month = datetime.date(year=2013, month=12, day=5)
        got = get_next_month(start_month)
        expected = datetime.date(year=2014, month=1, day=1)
        self.assertEqual(expected, got)

    def test_net_promoter_score_calculation(self):
        promoters = 50
        detractors = 25
        passive = 25
        nps = count_score(promoters, detractors, passive)
        self.assertEqual(float(25.0), nps)