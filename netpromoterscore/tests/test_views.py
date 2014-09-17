import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.urlresolvers import reverse
from netpromoterscore.models import PromoterScore


class TestPromoterScoreApiViews(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='jared', email='jared@hotmail.com', password='foobar123')
        self.user.save()
        self.client.login(username=self.user.username, password='foobar123')

    def test_promoter_score_returned_for_new_checked_out_customer(self):
        resp = self.client.get(reverse('retrieve_survey'))

        self.assertIn('true', resp.content)

    def test_promoter_score_returned_for_user_with_score_6_months_later(self):
        ps = PromoterScore(user=self.user, score=None)
        ps.save()
        ps.created_at = ps.created_at+datetime.timedelta(-7*365/12)
        ps.save()
        resp = self.client.get(reverse('retrieve_survey'))

        self.assertIn('true', resp.content)

    def test_update_score_reason(self):
        reason = 'Awesome!'

        score = PromoterScore(user=self.user, score=10)
        score.save()

        self.client.post(reverse('update_score_reason'), {'score_id': score.pk, 'reason': reason})

        score = PromoterScore.objects.get(pk=score.pk)
        self.assertEqual(score.reason, reason)

