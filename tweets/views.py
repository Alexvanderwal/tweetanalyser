from django.http import HttpResponse, JsonResponse
from django.template import loader
from tweets.models import Tweet
from tweets.service.streamcontroller import StreamController
from tweets.service.streaminformation import openstreams, lastupdates
from django.utils import timezone
from django.core import serializers


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

def update(request, uuid):
    print(openstreams)
    users_stream = openstreams.get(uuid)
    hashtag = users_stream.stream.hashtag
    print(hashtag)
    try:
        time = lastupdates.get(uuid)
        tweets = Tweet.tweets.filter(date_time__gt=time, hashtag=hashtag)
        lastupdates[uuid] = timezone.now()
    except:
        tweets = Tweet.tweets.filter(hashtag=hashtag)
        lastupdates[uuid] = timezone.now()
    tweets = serializers.serialize('json', tweets)
    return HttpResponse(tweets, content_type="application/json")