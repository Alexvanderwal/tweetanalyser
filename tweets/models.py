from django.core import serializers
from django.db.models import Avg
from django.utils import timezone

from django.db import models

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=30, unique=True)
    last_activated = models.DateTimeField()
    hashtags = models.Manager()

    def tweet_amount(self):
        return self.tweet_set.count()

    def avg_sentiment(self):
        if self.tweet_set.count() == 0 : return "neutral"
        avg = (self.tweet_set.aggregate(Avg('sentiment_score')))
        avg = ("%.2f" % avg['sentiment_score__avg'])
        # wat de fuck klopt hier niet??
        test = Sentiment.sentiments.filter(
            minimum_sentiment__lte=avg).order_by(
            'minimum_sentiment').last().name
        return test

    def __str__(self):
        return '#' + str(self.hashtag)

class Sentiment(models.Model):
    name = models.CharField(max_length=50)
    minimum_sentiment = models.DecimalField(max_digits=5,decimal_places=2)

    sentiments = models.Manager()

    def __str__(self):
        return str(self.name)


class Tweet(models.Model):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    sentiment_score = models.DecimalField(max_digits=5,decimal_places=2)
    sentiment_name = models.ForeignKey(Sentiment, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=300)
    date_time = models.DateTimeField()

    tweets = models.Manager()

    # Define what items to print upon being called through the manage.py shell
    def __str__(self):
        return '#' + str(self.hashtag.hashtag) + ' - score ' + str(self.sentiment_score)





