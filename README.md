# Django Net Promoter Score #

Django Net Promoter Score is designed to help you find out what your customers think of your application. The net promoter score metric is based on user feedback to one question, "On a scale from 1 to 10 how likely are you to recommend us to a friend or colleague?". You can jazz this question up to fit your projects needs, and use Django Net Promoter Score to keep track of user response and detect when it is time to ask a user the question again. Django Net Promoter Score also features an administrative page that displays a breakdown of the net promoter score metric over a 13 month period.

## Installation ##

Few simple steps:

 - Install `django-netpromoterscore` package:

        $ pip install django-netpromoterscore

 - Add `netpromoterscore` to your `INSTALLED_APPS`

 - Add urls to your urls.py:

        urlpatterns = patterns('',
            ...
            url(r'^api/survey/$', SurveyView.as_view(), name='survey'),
            url(r'^admin/net-promoter-score/', NetPromoterScoreView.as_view(), name='net-promoter-score'),
            ...
        )

- You are done!

## API ##

    GET /api/survey/

Returns `{ "survey_is_needed": true_or_false }`

    POST /api/survey/

With json POST data without `"id"` like `{ "score": 9 }` creates new PromoterScore instance for current user.

If `"id"` is provided and POST data is like `{ "id": 15, "reason": "Awesome!"}`, updates existing PromoterScore instance.

Returns `{ "id": PROMOTER_SCORE_ID }`

## Information on NPS Metric ##
There is some fantastic information available online to help you understand the NPS metric and how to use it to create healthier relationships with your users.

The [Brain & Company website](http://netpromotersystem.com/ "Title") is a handy resource for gaining insight into your applications net promoter score.

## Features ##
__Administrative Page__
![net promoter score administrative page][id]
[id]: http://i.imgur.com/lwI4W5K.png "Net Promoter Score Admin Page"
