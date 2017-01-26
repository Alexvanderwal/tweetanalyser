from rest_framework import serializers

from .models import Hashtag, Sentiment, Tweet


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        tweet_amount = serializers.SerializerMethodField('tweet_amount')
        avg_sentiment = serializers.SerializerMethodField('avg_sentiment')
        fields = ('id', 'hashtag', 'last_activated', 'tweet_amount', 'avg_sentiment')


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
