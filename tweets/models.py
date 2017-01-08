from django.db import models

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=30, unique=True)
    hashtags = models.Manager()

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





