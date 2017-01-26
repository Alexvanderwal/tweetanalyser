from django.contrib import admin

from .models import Tweet, Sentiment, Hashtag

admin.site.register(Tweet)
admin.site.register(Sentiment)
admin.site.register(Hashtag)
