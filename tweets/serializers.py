from rest_framework import serializers
from .models import Hashtag, Sentiment, Tweet

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id','hashtag')


class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentiment
        fields = ('id', 'name')


class TweetSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer()
    sentiment_name = SentimentSerializer()
    class Meta:
        model = Tweet
        fields = ('hashtag', 'sentiment_name')