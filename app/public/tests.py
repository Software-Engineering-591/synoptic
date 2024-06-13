from django.test import TestCase  # noqa: F401
from django.test import Client 
# Create your tests here.


# Testing if getting the webpages listed below returns true
# The status code must be 200 if self.assertTrue is valid
class WebpageTest(TestCase):

    def setUp(self):
        self.c = Client()
    # Testing for index response code 200
    def test_index(self):
        response = self.c.get('', follow=True)
        self.assertTrue(response.status_code == 200)
    # Testing for alert page response code 200
    def test_alert(self):
        response = self.c.get('/alert/', follow=True)
        self.assertTrue(response.status_code == 200)
    # Testing for weather page response code 200
    def test_weather(self):
        response = self.c.get('/weather/', follow=True)
        self.assertTrue(response.status_code == 200)
    # Testing for daily weather page response code 200
    def test_daily_weather(self):
        response = self.c.get('/daily_weather/', follow=True)
        self.assertTrue(response.status_code == 200)
    # Testing for weekly weather page response code 200
    def test_weekly_weather(self):
        response = self.c.get('/weekly_weather/', follow=True)
        self.assertTrue(response.status_code == 200)
    # Testing for our goals page response code 200
    def test_goals(self):
        response = self.c.get('/goals/', follow=True)
        self.assertTrue(response.status_code == 200)
    # Testing settings page response code 200
    def test_settings(self):
        response = self.c.get('/settings', follow=True)
        self.assertTrue(response.status_code == 200)