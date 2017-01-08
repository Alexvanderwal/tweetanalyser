import tweepy
import json
from tweepy.streaming import StreamListener
from tweets.models import Tweet
import html
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from .tweetprocessor import tokenize, pos_tag
from .tweetanalyser import Analyser
from queue import Queue
from threading import Thread
from multiprocessing import Pool
from django.contrib.staticfiles.templatetags.staticfiles import static as _static
import threading

class StreamerWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.analyser = Analyser()

    def run(self):
        while True:
            #get work from the queue and expand the tuple
            data, keyword = self.queue.get()
            tweet = self.construct_tweet(json.loads(html.unescape(data)), keyword)
            tokens = pos_tag(tokenize(tweet.tweet))
            tweet.sentiment_score = self.analyser.analyse(tokens)
            print(tweet)
            self.queue.task_done()

    # Create a object out of the tweet data to streamline the data handeling process
    def construct_tweet(self, data, keyword):
        date = self.to_datetime(str(data['created_at']))
        return Tweet(keyword=keyword, tweet=data['text'], date_time=date)

    # ?Uitzoeken wat dit doet
    def to_datetime(self, datestring):
        time_tuple = parsedate_tz(datestring.strip())
        dt = datetime(*time_tuple[:6])
        return dt - timedelta(seconds=time_tuple[-1])


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

    # Function that gets called on arrival of a new tweetc
    def on_data(self, data):

        self.queue.put((data, self.keyword))
        self.queue.join()
        return True

    def save_keyword(self, keyword):
        self.keyword = keyword
