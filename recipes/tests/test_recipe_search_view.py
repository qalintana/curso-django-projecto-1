from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeViewSearchTest(RecipeTestBase):

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_searh_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_scaped(self):
        url = reverse('recipes:search') + '?q=teste'
        response = self.client.get(url)
        self.assertIn('Pesquisa por teste', response.content.decode('utf-8'))

        title = 'This is recipe one'
        title_two = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title, user={'username': 'one'})
        recipe2 = self.make_recipe(
            slug='two', title=title_two, user={'username': 'two'})

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title}')
        response2 = self.client.get(f'{search_url}?q={title_two}')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])
