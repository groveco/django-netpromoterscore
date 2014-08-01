import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from promoterscore.models import PromoterScore
from django.core.urlresolvers import reverse


class TestPromoterScore(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jared', email='jared@hotmail.com', password='foobar123')
        self.user.save()
        self.client.login(username=self.user.username, password='foobar123')

    def test_promoter_score_returned_for_new_checked_out_customer(self):
        resp = self.client.get(reverse('promoter-score-get-survey'))

        self.assertIn('true', resp.content)

    def test_promoter_score_returned_for_user_with_score_6_months_later(self):
        ps = PromoterScore(user=self.user, score=None)
        ps.save()
        ps.created_at = ps.created_at+datetime.timedelta(-7*365/12)
        ps.save()
        resp = self.client.get(reverse('promoter-score-get-survey'))

        self.assertIn('true', resp.content)