from django.http import HttpResponse
from django.template import loader

from website.service.streamcontroller import StreamController
from website.service.streaminformation import openstreams


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