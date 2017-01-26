import html
import json
from queue import Queue
from threading import Thread

from django.utils import timezone
from tweepy.streaming import StreamListener

from tweets.models import Tweet, Hashtag, Sentiment
from .tweetanalyser import Analyser
from .tweetprocessor import TweetProcessor


class StreamerWorker(Thread):
    """
   Create the base for our worker Threads that will be responsible for
   delegating the data fetched by the stream to the different components used in the
   analysis process.
    """

    def __init__(self, queue):
        Thread.__init__(self)
        # Queue our worker will fetch his tasks from
        self.queue = queue
        self.analyser = Analyser()
        self.tweet_processor = TweetProcessor()

    def run(self):
        """
        Pick the first task from the queue heap and start the stripping process
        :return:
        """
        while True:
            data, hashtag = self.queue.get()
            self.construct_tweet(json.loads(html.unescape(data)), hashtag)
            self.queue.task_done()

    def construct_tweet(self, data, hashtag):
        """
        Use the information of data we actually are gonna use in the analysis
        and create a Tweet object from this
        :param data: The raw tweet as received from the stream
        :param hashtag: A hashtag object relevant to the search query
        :return:
        """
        date = timezone.now()
        # Try & catch to prevent crashing when a tweet is not sent correctly
        try:
            tweet = Tweet(hashtag=hashtag, tweet=data['text'], date_time=date)
            processed_tweet = self.tweet_processor.process_tweet(tweet.tweet)
            tweet.sentiment_score = self.analyser.analyse(processed_tweet)
            tweet.sentiment_name = Sentiment.sentiments.filter(
                minimum_sentiment__lte=tweet.sentiment_score).order_by(
                'minimum_sentiment').last()
            tweet.save()
            # Broad exception here because we dont really care what kind of error it is
        except:
            print("error")


class Streamer(StreamListener):
    """
    Uses the tweepy StreamListener to fetch all new teets which contain the
    hashtag object relevant to the search query
    """

    # Create a queue to communicate with the worker threads
    queue = Queue()
    for x in range(8):
        worker = StreamerWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    def on_data(self, data):
        """
        Function that gets called by StreamListener everytime a new tweet comes in
        :param data: the new tweet in question
        :return: signal if there were problems with the tweet
        """
        try:
            self.queue.put((data, self.hashtag))
            self.queue.join()
            return True
        except:
            return False

    def save_hashtag(self, hashtag):
        """
        Create a hashtag object with the hashtag(text) the user queried with
        so we can reference this throughout the streaming process
        :param hashtag: Hashtag string
        :return:
        """
        try:
            self.hashtag = Hashtag.hashtags.get(hashtag=hashtag)
            self.hashtag.last_activated = timezone.now()
        except Hashtag.DoesNotExist:
            self.hashtag = Hashtag(hashtag=hashtag, last_activated=timezone.now())
        self.hashtag.save()
