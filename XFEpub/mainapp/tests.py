from django.test import TestCase
from mainapp.views import api_webscrape_call
# Create your tests here.
class webTestCase(TestCase):
    def test(self):
        api_webscrape_call()
