from collections import defaultdict

from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time',\
        'preparation_time_unit', 'servings', 'servings_unit', \
        'preparation_steps', 'cover'

        widgets = {
                'cover': forms.FileInput(
                    attrs={
                        'class': 'span-2'
                    }
                ),
                'servings_unit': forms.Select(
                    choices=(
                        ('Porções', 'Porções'),
                        ('Pedaços', 'Pedaços'),
                        ('Pessoas', 'Pessoas'),
                    ),
                ),
                'preparation_time_unit': forms.Select(
                    choices=(
                        ('Minutos', 'Minutos'),
                        ('Horas', 'Horas'),
                    ),
                ),
            }
        
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cd = self.cleaned_data
        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self._my_errors['title'].append('Cannot be equal to description')
            self._my_errors['description'].append('Cannot be equal to title')

        if self._my_errors:
            raise forms.ValidationError(self._my_errors)
        return super_clean
    
    def clean_title(self):
        title = self.cleaned_data

        if len(title) < 5:
            self._my_errors['title'].append(
                'Title must have at least 5 chars.'
            )

        return title
    
    def clean_preparation_time(self):
        field_value = self.cleaned_data.get('preparation_time')

        if is_positive_number(field_value):
            self._my_errors['preparation_time'].append(
                'Must be a positive number'
            )

        return field_value
    
    def clean_servings(self):
        field_value = self.cleaned_data.get('servings')

        if is_positive_number(field_value):
            self._my_errors['servings'].append(
                'Must be a positive number'
            )

        return field_value