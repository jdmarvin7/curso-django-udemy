
from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class RecipeDetailTest(RecipeTestBase):

    def test_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes-recipe', kwargs={'pk': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes-recipe', kwargs={'pk': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes-recipe', args=(1000,))
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
            self.make_recipe(title='This is a detail page - It load one recipe')
            
            response = self.client.get(reverse('recipes-recipe', args=(1,)))
            content = response.content.decode('utf-8')

            self.assertIn('This is a detail page - It load one recipe', content)

    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        """ Testando se vai publicar recipe caso não seja publicado """
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes-recipe', kwargs={
             'pk': recipe.pk
        }))
        self.assertEqual(response.status_code, 404)