from django.test import TestCase
from django.urls import reverse

class RecipeURLsTest(TestCase):
    def test_the_pytest_is_ok(self):
        assert 1 == 1, 'Um é igual a um'

    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes-home')
        self.assertEqual(home_url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes-category', kwargs={'category_id': 1,})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_url_is_correct(self):
        url = reverse('recipes-recipe', args=(1, ))
        self.assertEqual(url, '/recipes/1/')