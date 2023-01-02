from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe
from recipes.tests.test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found here ',
                      response.content.decode('utf-8'),
                      )

        # self.fail('Para que eu termine de digita-lo')

    def test_recipe_home_template_load_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('10 Minutos', content)
        self.assertIn('Recipe title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_published(self):
        """Test recipe is published False dont show"""
        Recipe.objects.get(pk=1).delete()
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('No recipes found here ',
                      response.content.decode('utf-8'),
                      )
