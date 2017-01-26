from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tweets.models import Tweet, Hashtag
from tweets.service.streamcontroller import StreamController
from tweets.service.streaminformation import openstreams, lastupdates
from .serializers import TweetSerializer, HashtagSerializer


def index(request):
    template = loader.get_template('tweets/index.html')
    return HttpResponse(template.render(request))


def start_stream(request, uuid, hashtag):
    template = loader.get_template('tweets/index.html')
    active_stream = StreamController(uuid, hashtag)
    active_stream.run()
    return HttpResponse(template.render(request))


def stop_stream(request, uuid):
    template = loader.get_template('tweets/index.html')
    active_stream = openstreams.get(uuid)
    active_stream.stop()
    return HttpResponse(template.render(request))


@api_view(['GET'])
def old_queries(request):
    """
    Sends 4 old searched on hashtags to the front end
    :param request:
    :return:
    """
    hashtags = Hashtag.hashtags.all()[:4]
    serializer = HashtagSerializer(hashtags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def update(request, uuid):
    """
    Sends all new analysed records in the database to the Frontend
    :param request:
    :param uuid: Unique User Id identifying which stream belongs to the requesting user
    :return:
    """
    hashtag = ''
    try:
        users_stream = openstreams.get(uuid)
        hashtag = users_stream.stream.hashtag
    except:
        print('error')
    try:
        time = lastupdates.get(uuid)
        tweets = Tweet.tweets.filter(date_time__gt=time, hashtag=hashtag)
        lastupdates[uuid] = timezone.now()
    except:
        tweets = Tweet.tweets.filter(hashtag=hashtag)
        lastupdates[uuid] = timezone.now()
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)

