from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    # recipes = get_list_or_404(Recipe.objects.filter(is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })

def recipe(request, id): 
    # recipe =Recipe.objects.filter(
    #     pk=id, 
    #     is_published=True
    # ).order_by('-id').first()

    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })

def category(request, category_id):
    # recipes = Recipe.objects.filter(
    #     category__id=category_id, 
    #     is_published=True
    # ).order_by('-id')

    recipes = get_list_or_404(Recipe, category_id=category_id,
        is_published=True,
    )

    # category_name = getattr(
    #     getattr(recipes.first(), 'category', None),
    #     'name',
    #     'Not found'
    # )

    # if not recipes:
    #     raise Http404('Not found')

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
    })