import datetime
from rest_framework import serializers
from models import PromoterScore


class PromoterScoreSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='pk')
    score = serializers.Field(source='score')

    class Meta:
        model = PromoterScore