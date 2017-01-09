from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    #/tweets/
    url(r'^$', views.index, name='tweets'),
    #/tweets/stream/status
    url(r'^stream/(?P<uuid>.*)/(?P<hashtag>\w{0,50})$', views.start_stream, name='stream'),
    url(r'^stop/stream/(?P<uuid>.*)$', views.stop_stream, name='stop_stream'),
    url(r'^update/(?P<uuid>.*)/$', views.update, name='update')
]

#Allows us to format the data in whatever type we want
urlpatterns = format_suffix_patterns(urlpatterns)
