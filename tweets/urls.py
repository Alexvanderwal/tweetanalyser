from django.conf.urls import url, include
from . import views
urlpatterns = [
    #/tweets/
    url(r'^$', views.index, name='tweets'),
    #/tweets/stream/status
    url(r'^stream/(?P<uuid>.*)/(?P<hashtag>\w{0,50})$', views.start_stream, name='stream'),
    url(r'^stop/stream/(?P<uuid>.*)', views.stop_stream, name='stop_stream')
]