from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self, first_name='user',
                    last_name='name',
                    username='nomeusuario',
                    password='123456',
                    email='alintana@alintana.co'):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email)

    def make_recipe(self,
                    title='Recipe title',  description='recipe description',
                    slug='recipe-title', preparation_time=10,
                    preparation_time_unit='Minutos', servings=5,
                    servings_unit='porçoes',
                    preparation_step='Recipe preparation step',
                    preparation_step_is_html=False,
                    is_published=True, category=None, user=None):

        if category is None:
            category = {}

        if user is None:
            user = {}

        return Recipe.objects.create(  # noqa
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
            category=self.make_category(**category),
            user=self.make_author(**user))
