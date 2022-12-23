from django.test import TestCase
from mainapp.views import webScrape
# Create your tests here.
class webTestCase(TestCase):
    def test(self):
        webScrape()
