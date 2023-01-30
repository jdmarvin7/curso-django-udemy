from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class RecipeSearchViewTest(RecipeTestBase):
    
    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes-search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes-search'))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes-search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_search_uses_correct_view_template(self):

        response = self.client.get(reverse('recipes-search') + '?q="d"')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    