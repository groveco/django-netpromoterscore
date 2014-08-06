import datetime
from django.test import TestCase
from promoterscore.utils import get_many_previous_months


class TestUtils(TestCase):

    def test_get_many_previous_months(self):
        start_month = datetime.date(year=2014, month=9, day=21)
        got = get_many_previous_months(month=start_month, total_months=3)
        expected = [datetime.date(year=2014, month=8, day=1), datetime.date(year=2014, month=7, day=1), datetime.date(year=2014, month=6, day=1)]
        self.assertEqual(expected, got)