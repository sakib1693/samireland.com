from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
         username="testsam",
         password="testpassword"
        )
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(350, 600)


    def tearDown(self):
        self.browser.quit()


    def login(self):
        self.client.login(username="testsam", password="testpassword")
        cookie = self.client.cookies["sessionid"].value
        self.browser.get(self.live_server_url + "/")
        self.browser.add_cookie({
         "name": "sessionid", "value": cookie, "secure": False, "path": "/"
        })
        self.browser.refresh()
