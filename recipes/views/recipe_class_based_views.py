import os
from django.http import Http404
from django.views.generic import ListView, DetailView

from django.db.models import Q
from recipes.models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination
PER_PAGE = int(os.environ.get('PER_PAGES', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = qs.filter(
            is_published=True,
        )

        qs = qs.select_related('author', 'category')
        # qs = qs.prefetch_related('author', 'category')
        qs = qs.prefetch_related('tags')

        return qs
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, context.get('recipes'), PER_PAGE)

        context.update({ 'recipes': page_obj, 'pagination_range': pagination_range })
        return context
    
class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        # search_term = self.request.GET.get('q', '')

        ctx.update({
            'title': f"{ctx.get('recipes')[0].category.name}"
        })

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()
        
        return qs
    
class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()
        
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        
        if not qs:
            raise Http404()
        
        qs.filter(
            is_published=True
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx
    
class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            tags__sulg=self.kwargs.get('slug', '')
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(sulg=self.kwargs.get('slug', ''))

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': f'Search for "{page_title}" |',
        })

        return ctx