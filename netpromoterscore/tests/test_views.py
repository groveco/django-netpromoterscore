import datetime
import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.urlresolvers import reverse
from netpromoterscore.models import PromoterScore


class TestPromoterScoreApiViews(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='jared', email='jared@hotmail.com', password='foobar123'
        )
        self.user.save()
        self.client.login(username=self.user.username, password='foobar123')
        PromoterScore.objects.all().delete()

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
