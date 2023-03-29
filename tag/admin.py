from django.contrib import admin
from .models import Tag

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug'
    list_display_links = 'slug', 'id'
    search_fields = 'id', 'slug', 'name'
    list_per_page = 10
    list_editable = 'name',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',)
    }