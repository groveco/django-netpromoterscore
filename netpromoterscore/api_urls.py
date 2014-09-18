from django.conf.urls import patterns, url
from .views import SurveyView

urlpatterns = patterns('',
    url(r'survey/$', SurveyView.as_view(), name='survey'),
)
