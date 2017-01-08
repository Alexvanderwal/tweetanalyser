from tweepy import OAuthHandler
from django.conf import settings

#Instance of the OAuthHandler for our twitter streams
auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

#Dictionairy which keeps track of all open streams, so we can make sure the program doesnt keep any "old" streams open
openstreams = {}

