import datetime
from django.test import TestCase
from promoterscore.models import PromoterScore
from pypantry.tests.factories import CustomerFactory
from django.core.urlresolvers import reverse
from django.conf import settings
from testsupport import create_socialapp


class TestPromoterScore(TestCase):

    def setUp(self):
        create_socialapp()
        self.customer = CustomerFactory()

    def do_req(self, login=True):
        if login:
            self.client.login(username=self.customer.email, password=settings.CUSTOMER_PASSWORD)
        resp = self.client.get(reverse('promoter-score'))
        return resp

    def test_promoter_score_returned_for_new_checked_out_customer(self):
        response = self.do_req()

        self.assertIn('<input name="score" type="radio" value="3"', response.content)

    def test_promoter_score_returned_for_customer_with_score_6_months_later(self):
        ps = PromoterScore(customer=self.customer, taken_at=datetime.datetime.now()+datetime.timedelta(-7*365/12), score=None)
        ps.save()
        response = self.do_req()

        self.assertIn('<input name="score" type="radio" value="3"', response.content)