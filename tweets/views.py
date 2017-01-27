from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tweets.models import Hashtag
from tweets.service.streamcontroller import StreamController
from tweets.service.streaminformation import openstreams
from .serializers import HashtagSerializer


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
    Sends 3 old searched on hashtags to the front end
    :param request:
    :return:
    """
    hashtags = Hashtag.hashtags.all().order_by('-last_activated')[:3]
    serializer = HashtagSerializer(hashtags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def update(request, uuid):
    active_stream = openstreams.get(uuid).stream.hashtag
    serializer = HashtagSerializer(active_stream, many=False)
    return Response(serializer.data)

