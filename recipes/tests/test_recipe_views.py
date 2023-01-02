from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.models import Category, Recipe, User

# Create your tests here.


class RecipeViewsTest(TestCase):
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
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found here',
                      response.content.decode('utf-8'),
                      )

    def test_recipe_home_template_load_recipes(self):
        category = Category.objects.create(name='Category')
        user = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='alintana@alintana.co')

        recipe = Recipe.objects.create(  # noqa
            title='Recipe title',
            description='recipe description',
            slug='recipe-title',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='porçoes',
            preparation_step='Recipe preparation step',
            preparation_step_is_html=False,
            is_published=True,
            category=category,
            user=user)

        response = self.client.get(reverse('recipes:home'))
        response_recipe = response.context['recipes']
        self.assertEqual(response_recipe.first().title, 'Recipe title')

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_not_recipe_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_not_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
