from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class FunctionalTest(TestCase):
    
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.browser = webdriver.Chrome(options=chrome_options)

    def test_can_see_homepage(self):
        self.browser.get('http://localhost:8001')
        self.assertIn('Home', self.browser.title)

    def tearDown(self):
        self.browser.quit()