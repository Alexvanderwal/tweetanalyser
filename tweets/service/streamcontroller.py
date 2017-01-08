from tweepy import Stream

from tweets.service.streaminformation import auth, openstreams
from .streamer import Streamer
from tweets.models import Hashtag


class  StreamController():
    def __init__(self, unique_user_id, keyword):
        #Assign the pre instanciated auth object to instanciate the controller
        #This way we dont have to create a new auth object for each controller
        self.auth = auth
        self.unique_user_id = unique_user_id
        self.hashtag = keyword
        openstreams[self.unique_user_id] = self


    def run(self):
        self.stream = Streamer()
        self.stream.save_hashtag(self.hashtag)
        self.twitter_stream = Stream(self.auth, self.stream)
        self.twitter_stream.filter(track=['#{0}'.format(self.hashtag)], languages=["en"], async=True)


    def stop(self):
        self.twitter_stream.disconnect()
