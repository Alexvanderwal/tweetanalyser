from django.http import HttpResponse, JsonResponse
from django.template import loader
from tweets.models import Tweet, Hashtag
from tweets.service.streamcontroller import StreamController
from tweets.service.streaminformation import openstreams, lastupdates
from django.utils import timezone
from django.core import serializers
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    hashtags = Hashtag.hashtags.all()[:3]
    serializer = HashtagSerializer(hashtags, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def update(request, uuid, format=None):
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

