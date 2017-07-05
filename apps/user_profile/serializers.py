from rest_framework import serializers


class UserDetailsSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    avatar_url = serializers.CharField(required=False)
    user_tweets = serializers.CharField(required=False)


