# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-08 22:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=30, unique=True)),
            ],
            managers=[
                ('hashtags', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Sentiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('minimum_sentiment', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            managers=[
                ('sentiments', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentiment_score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tweet', models.CharField(max_length=300)),
                ('date_time', models.DateTimeField()),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweets.Hashtag')),
                ('sentiment_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweets.Sentiment')),
            ],
            managers=[
                ('tweets', django.db.models.manager.Manager()),
            ],
        ),
    ]
