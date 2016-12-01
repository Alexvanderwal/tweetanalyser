import tweepy
import json
from tweepy.streaming import StreamListener
from tweets.models import Tweets
import html
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from .tweetsanitizer import sanitize
class Streamer(StreamListener):
    isactive = True
    #Function that gets called on arrival of a new tweet
    def on_data(self, status):
        if self.isactive == True:
            tweet = self.construct_tweet(json.loads(html.unescape(status)),  self.keyword)
            tokens = sanitize(tweet.tweet)
            return True
        else:
            return False

    #Ensures that we can submit the keyword to the streamer object without it overriding the other streamer object
    def registerKeyword(self, keyword):
        self.keyword = keyword

    #Create a object out of the tweet data to streamline the data handeling process
    def construct_tweet(self, status, keyword):
        date= self.to_datetime(str(status['created_at']))
        return Tweets(status['text'], date, keyword)

    def to_datetime(self, datestring):
        time_tuple = parsedate_tz(datestring.strip())
        dt = datetime(*time_tuple[:6])
        return dt - timedelta(seconds=time_tuple[-1])

    def save_keyword(self, keyword):
        self.keyword = keyword


