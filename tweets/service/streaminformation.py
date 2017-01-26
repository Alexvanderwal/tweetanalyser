from django.conf import settings
from tweepy import OAuthHandler

#Instance of the OAuthHandler for our twitter streams
auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

# Dictionairy which keeps track of all open streams,
# so we can make sure the program doesnt keep any "old" streams open
openstreams = {}

# Dictionairy which keeps track of the last database request made by
# the user his browser to keep the query as small as possible
lastupdates = {}
