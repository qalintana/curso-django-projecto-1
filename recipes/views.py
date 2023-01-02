from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe


# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(
        is_published=True).order_by('-id')

    return render(request, 'recipes/pages/home.html', status=200,
                  context={'recipes': recipes})


def category(request: HttpRequest, category_id: int) -> HttpResponse:
    # recipes = Recipe.objects.filter(
    #     category__id=category_id, is_published=True)

    # if not recipes:
    #     raise Http404('Not found 😢')
    # category_name = getattr(
    #     getattr(recipes.first(), 'category', None), 'name', 'Not found')

    # recipes = get_list_or_404(
    #     Recipe, category__id=category_id, is_published=True)
    # print(recipes)

    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    return render(
        request, 'recipes/pages/category.html',
        status=200,
        context={'recipes': recipes,
                 'title': f'{recipes[0].category.name} - Category'}
    )


def recipe(request: HttpRequest, id: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(
        request, 'recipes/pages/recipe-view.html',
        status=200,
        context={'recipe': recipe, 'is_detail_page': True}
    )


def search(request: HttpRequest):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q
        (
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True).order_by('-id')

    recipes = recipes.filter(is_published=True)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Pesquisa por { search_term }',
        'search_term': search_term,
        'recipes': recipes
    })
