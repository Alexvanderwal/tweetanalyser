from django.test import TestCase, RequestFactory

from .models import Sentiment
from .views import start_stream, stop_stream, update, old_queries


class streamTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 3942931923
        self.keyword = "Python"

    def test_start_stream(self):
        # Create an instance of a GET request.
        request = self.factory.get('/stream/{0}/{1}'.format(self.uuid, self.keyword))

        # Test start_stream as if it were deployed at /stream/uuid/keyword
        response = start_stream(request, self.uuid, self.keyword)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        # Create an instance of a GET request.
        request = self.factory.get('/update/{0}'.format(self.uuid))

        # Test update as if it were deployed at /update/uuid
        response = update(request, self.uuid)
        self.assertEqual(response.status_code, 200)

    def test_stop_stream(self):
        # Create an instance of a GET request.
        request = self.factory.get('stop/stream/{0}'.format(self.uuid))

        # Test stop_stream as if it were deployed at /stop/stream/uuid
        response = stop_stream(request, self.uuid)
        self.assertEqual(response.status_code, 200)

    def test_oldqueries(self):
        # Create an instance of a GET request.
        request = self.factory.get('oldqueries/')

        # Test start_stream as if it were deployed at /oldqueries
        response = old_queries(request)
        self.assertEqual(response.status_code, 200)


class modelTests(TestCase):
    def setUp(self):
        self.Sentiment = Sentiment(name="Positive", minimum_sentiment="1.00")

    def test_sentiment(self):
        self.assertEqual(self.Sentiment.name, "Positive")
