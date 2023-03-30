import os
from django.db import models
from collections import defaultdict
from django.forms import ValidationError
from django.conf import settings

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField(blank=True)
    preparation_steps_is_html = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
        default=None
    )
    # tags = GenericRelation(Tag, related_query_name='recipes')
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("recipes-recipe", args=(self.id,))
    
    @staticmethod
    def resize_image(image, new_width):
        img_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(img_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            img_full_path,
            optimize=True,
            quality=50,
        )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug
        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...

        return saved
    
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)
        
    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
    