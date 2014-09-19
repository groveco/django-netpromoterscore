import datetime
import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from netpromoterscore.models import PromoterScore
from netpromoterscore.views import NetPromoterScoreView
from . import TestMixin


class TestPromoterScoreApiViews(TestCase, TestMixin):

    def setUp(self):
        self.create_users()
        self.client.login(username=self.user.username, password='foobar123')

    def tearDown(self):
        self.delete_promoter_scores()
        self.delete_users()

    def test_promoter_score_returned_for_new_checked_out_customer(self):
        response = self.client.get(reverse('survey'))
        data = json.loads(response.content)

        self.assertEqual(data['survey_is_needed'], True)

    def test_promoter_score_returned_for_user_with_score_6_months_later(self):
        ps = PromoterScore(user=self.user, score=None)
        ps.save()
        ps.created_at = ps.created_at - datetime.timedelta(7*30)
        ps.save()

        response = self.client.get(reverse('survey'))
        data = json.loads(response.content)

        self.assertEqual(data['survey_is_needed'], True)

    def test_survey_view_create_score(self):
        score = 10
        data = json.dumps({'score': score})

        response = self.client.post(reverse('survey'), data, content_type='application/json')
        pk = int(json.loads(response.content)['id'])
        created = PromoterScore.objects.get(pk=pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(created.user, self.user)
        self.assertEqual(created.score, score)

    def test_survey_view_update_reason(self):
        reason = 'Awesome!'

        promoter_score = PromoterScore(user=self.user, score=10)
        promoter_score.save()

        data = json.dumps({'id': promoter_score.pk, 'reason': reason})
        response = self.client.post(reverse('survey'), data, content_type='application/json')
        print response.content

        promoter_score = PromoterScore.objects.get(pk=promoter_score.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(promoter_score.reason, reason)


class TestNetPromoterScoreView(TestCase, TestMixin):

    def setUp(self):
        self.create_users()
        self.create_promoter_scores()

        self.view_instance = NetPromoterScoreView()

    def tearDown(self):
        self.delete_promoter_scores()
        self.delete_users()

    def test_get_netpromoter_with_rolling(self):
        expected = [1, 1]
        got = self.view_instance.get_netpromoter(month=self.now, rolling=True)
        self.assertEqual(expected, [got['promoters'], got['passive']])

    def test_get_netpromoter_without_rolling(self):
        expected = [0, 1]
        got = self.view_instance.get_netpromoter(month=self.now, rolling=False)
        self.assertEqual(expected, [got['promoters'], got['passive']])