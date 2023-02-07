from django.test import TestCase
from mainapp.views import api_webscrape_call
import timeit
# Create your tests here.
class webTestCase(TestCase):
    def test(self):
        print(timeit.timeit(api_webscrape_call, number=1))
