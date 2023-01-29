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

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes-category', args=(1,)))
        self.assertIs(view.func, views.category)

    def test_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes-recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
    
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

    def test_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes-recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        self.make_recipe(title='This is a detail page - It load one recipe')
        
        response = self.client.get(reverse('recipes-recipe', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn('This is a detail page - It load one recipe', content)

    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        """ Testando se vai publicar recipe caso não seja publicado """
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes-recipe', args=(recipe.id,)))
        self.assertEqual(response.status_code, 404)

    def test_recipe_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes-recipe', args=(1000,))
        )
        self.assertEqual(response.status_code, 404)