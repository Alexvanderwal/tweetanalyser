from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .views import start_stream, stop_stream, update, old_queries
class streamTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.uuid = 3942931923
        self.keyword = "Python"

    def test1(self):
        # Create an instance of a GET request.
        request = self.factory.get('/stream/{0}/{1}'.format(self.uuid, self.keyword))

        # Test start_stream as if it were deployed at /stream/uuid/keyword
        response = start_stream(request, self.uuid, self.keyword)
        self.assertEqual(response.status_code, 200)

    def test3(self):
        # Create an instance of a GET request.
        request = self.factory.get('/update/{0}'.format(self.uuid))

        # Test start_stream as if it were deployed at /stream/uuid/keyword
        response = update(request, self.uuid)
        self.assertEqual(response.status_code, 200)

    def test2(self):
        # Create an instance of a GET request.
        request = self.factory.get('stop/stream/{0}'.format(self.uuid))

        # Test start_stream as if it were deployed at /stream/uuid/keyword
        response = stop_stream(request, self.uuid)
        self.assertEqual(response.status_code, 200)

    def test4(self):
        # Create an instance of a GET request.
        request = self.factory.get('oldqueries/')

        # Test start_stream as if it were deployed at /stream/uuid/keyword
        response = old_queries(request)
        self.assertEqual(response.status_code, 200)





