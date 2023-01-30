from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase

class RecipeViewsTest(RecipeTestBase):
    # SETUP
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes-home'))
        self.assertIs(view.func, views.home)
    # TEARDOWN
    
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes-home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes-home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_show_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes-home'))
        self.assertIn(
            '<h1>No recipes founds here</h1>',
            response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes-home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('5 Porções', content)
        self.assertIn('10 Minutos', content)
        self.assertEqual(len(response_context_recipes), 1)
    
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """ Testando se vai publicar recipe caso não seja publicado """
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes-home'))
        content = response.content.decode('utf-8')

        self.assertIn('<h1>No recipes founds here</h1>', content)
