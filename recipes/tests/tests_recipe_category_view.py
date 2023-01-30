from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class RecipeCategoryTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes-category', args=(1,)))
        self.assertIs(view.func, views.category)

    def test_recipe_category_template_loads_recipes(self):
        self.make_recipe(title='This is a category test')
        
        response = self.client.get(reverse('recipes-category', args=(1,)))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('This is a category test', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """ Testando se vai publicar recipe caso não seja publicado """
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes-recipe', args=(recipe.category.id,)))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes-category', args=(1000,)))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes-category', args=(1000,))
        )
        self.assertEqual(response.status_code, 404)