from django.contrib import admin
from .models import Category, Recipe
from tag.models import Tag
from django.contrib.contenttypes.admin import GenericStackedInline

class CategoryAdmin(admin.ModelAdmin):
    ...
admin.site.register(Category, CategoryAdmin)

class TagInline(GenericStackedInline):
    model = Tag
    fields = 'name',
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published',)
    list_display_links = ['id', 'title', 'created_at']
    search_fields = 'id', 'title', 'description', 'slug'
    list_filter = 'category', 'author', 'is_published'
    list_per_page = 10
    list_editable = ('is_published',)
    ordering = 'id',
    prepopulated_fields = {
        "slug": ('title',)
    }
    inlines = [
        TagInline
    ]