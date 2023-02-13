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

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one',
            title=title1,
            author_data={'username': 'J D'}
        )

        recipe2 = self.make_recipe(
            slug='Two',
            title=title2,
            author_data={'username': 'Marvin'}
        )

        search_url = reverse('recipes-search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(response1, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(response2, response2.context['recipes'])

        self.assertNotIn(response1, response_both.context['recipes'])
        self.assertNotIn(response2, response_both.context['recipes'])
