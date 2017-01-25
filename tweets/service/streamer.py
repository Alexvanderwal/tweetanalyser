import tweepy
import json
from tweepy.streaming import StreamListener
from tweets.models import Tweet, Hashtag, Sentiment
import html
from .tweetprocessor import TweetProcessor
from .tweetanalyser import Analyser
from queue import Queue
from threading import Thread
from django.utils import timezone


class StreamerWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.analyser = Analyser()
        self.tweet_processor = TweetProcessor()

    def run(self):
        while True:
            #get work from the queue and expand the tuple
            data, hashtag = self.queue.get()
            self.construct_tweet(json.loads(html.unescape(data)), hashtag)
            self.queue.task_done()

    # Create a object out of the tweet data to streamline the data handeling process
    def construct_tweet(self, data, hashtag):
        date = timezone.now()
        #Try and catch incase the stream gets a tweet with a empty data['text'] so it doesn't exit the stream
        try:
            tweet = Tweet(hashtag=hashtag, tweet=data['text'], date_time=date)
            processed_tweet = self.tweet_processor.process_tweet(tweet.tweet)
            tweet.sentiment_score = self.analyser.analyse(processed_tweet)
            tweet.sentiment_name = Sentiment.sentiments.filter(
                minimum_sentiment__lte=tweet.sentiment_score).order_by(
                'minimum_sentiment').last()
            tweet.save()
        except:
            print("error")


class Streamer(StreamListener):
    # Create a queue to communicate with the worker threads
    queue = Queue()
    workerAmount = 8
    # Create 8 worker threads
    for x in range(workerAmount):
        worker = StreamerWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    # Function that gets called on arrival of a new tweet
    def on_data(self, data):

        self.queue.put((data, self.hashtag))
        self.queue.join()
        return True

    #Create the hashtag model object so we can reference it in our tweet objects
    def save_hashtag(self, hashtag):
        try:
            self.hashtag = Hashtag.hashtags.get(hashtag=hashtag)
            self.hashtag.last_activated = timezone.now()
        except Hashtag.DoesNotExist:
            self.hashtag = Hashtag(hashtag=hashtag, last_activated=timezone.now())
        print(self.hashtag)
        print(self.hashtag.avg_sentiment())
        self.hashtag.save()

