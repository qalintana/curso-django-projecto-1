from django.urls import resolve, reverse

from recipes import views
from recipes.models import Category, Recipe, User
from recipes.tests.test_recipe_base import RecipeTestBase

# Create your tests here.


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_not_recipe_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_load_recipes(self):
        needed_title = 'This is a category test'
        Category.objects.get(pk=1).delete()
        User.objects.get(pk=1).delete()
        Recipe.objects.get(pk=1).delete()

        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category',
                                           kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)
        ...
