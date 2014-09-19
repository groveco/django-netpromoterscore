from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from netpromoterscore.models import PromoterScore


class TestMixin(object):

    def create_users(self):
        self.user_model = get_user_model()

        self.user = self.user_model.objects.create_user(
            username='jared', email='jared@hotmail.com', password='foobar123'
        )
        self.user2 = self.user_model.objects.create_user(
            username='cole', email='cole@hotmail.com', password='foobar321'
        )

        self.user.save()
        self.user2.save()

    def create_promoter_scores(self):
        self.now = datetime.now()

        self.ps1 = PromoterScore(user=self.user, score=8)
        self.ps1.save()

        self.ps2 = PromoterScore(user=self.user, score=9)
        self.ps2.save()
        self.ps2.created_at = self.now - timedelta(4*365/12)
        self.ps2.save()

        self.ps3 = PromoterScore(user=self.user2, score=9)
        self.ps3.save()
        self.ps3.created_at = self.now - timedelta(7*365/12)
        self.ps3.save()

    def delete_users(self):
        self.user_model.objects.all().delete()

    def delete_promoter_scores(self):
        PromoterScore.objects.all().delete()