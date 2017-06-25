from rest_framework import serializers, views
from .models import LSTM


class LSTMSerializer(serializers.Serializer):
    model_input = serializers.CharField(required=True, allow_blank=False, max_length=10000)
    movie_year = serializers.IntegerField(required=False)
    rating = serializers.FloatField(required=False)

