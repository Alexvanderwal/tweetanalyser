from django.db import models

# Create your models here.
class Tweet(models.Model):
    keyword = models.CharField(max_length=30)
    sentiment_score = models.DecimalField(max_digits=5,decimal_places=2)
    tweet = models.CharField(max_length=300)
    date_time = models.DateTimeField()


# Define what items to print upon being called through the manage.py shell
    def __str__(self):
        return '#' + self.keyword + ' - score ' + str(self.sentiment_score)




class Sentiment(models.Model):
    name = models.CharField(max_length=10)
    minimum_sentiment = models.DecimalField(max_digits=5,decimal_places=2)


# class Tweets():
#     managed = False
#     tweet = ""
#     datetime = ""
#     sentiment = ""
#     keyword = ""
#
#     def __init__(self, tweet, datetime, keyword):
#         self.tweet = tweet
#         self.datetime = datetime
#         self.keyword = keyword
#         self.sentiment = 0






