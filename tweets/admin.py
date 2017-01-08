from django.contrib import admin
from .models import Tweet, Sentiment, Hashtag
# Register your models here.

admin.site.register(Tweet)
admin.site.register(Sentiment)
admin.site.register(Hashtag)
