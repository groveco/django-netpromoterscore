import datetime
from django.http import HttpResponse
from rest_framework import viewsets
from promoterscore.models import PromoterScore


class PromoterScoreApiView(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                score_raw = request.DATA.get('score', None)
                # If user does not enter score, set score to less than zero before request
                score = score_raw if score_raw > 0 else None
                created_at = datetime.datetime.now()
                promoter_score = PromoterScore(user=request.user, created_at=created_at, score=score)
                promoter_score.save()
                return HttpResponse("Promoter score successfully taken.")
            except Exception:
                return HttpResponse("Something went terribly wrong! So many dead bodies. There is blood everywhere.")

    def retrieve(self, request, *args, **kwargs):
        ps_queryset = PromoterScore.objects.filter(user=request.user)
        # get the most recent promoter score or None
        self.promoter_score = ps_queryset.order_by('created_at').reverse()[0] if ps_queryset else None

        if not self.promoter_score or self.time_to_ask() < datetime.datetime.now():
            return HttpResponse(
                content='<p>We love to hear from our friends! How likely are you to tell your friends about ePantry?</p> \
                    <ul> \
                        <li>Not at all likely.</li> \
                        <li><input name="score" type="radio" value="1" /> 1</li> \
                        <li><input name="score" type="radio" value="2" /> 2</li> \
                        <li><input name="score" type="radio" value="3" /> 3</li> \
                        <li><input name="score" type="radio" value="4" /> 4</li> \
                        <li><input name="score" type="radio" value="5" /> 5</li> \
                        <li><input name="score" type="radio" value="6" /> 6</li> \
                        <li><input name="score" type="radio" value="7" /> 7</li> \
                        <li><input name="score" type="radio" value="8" /> 8</li> \
                        <li><input name="score" type="radio" value="9" /> 9</li> \
                        <li><input name="score" type="radio" value="10" /> 10</li> \
                        <li>Very likely!</li> \
                    </ul>',
                content_type='text/html')
        else:
            return HttpResponse("Conditions not met for promoter score")

    def time_to_ask(self):
        return self.promoter_score.created_at.replace(tzinfo=None)+datetime.timedelta(6*365/12)