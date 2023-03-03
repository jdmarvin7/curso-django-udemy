import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest
from utils.browser import make_chrome_browser

class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        browser = self.browser
        browser.get(self.live_server_url)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)