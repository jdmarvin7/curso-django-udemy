from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized

class RecipeTestModel(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            is_published=False
        )
        recipe.save()
        recipe.full_clean()
        return recipe

    def test_recipe_title_raises_error_if_title_has_more_than_155_chars(self):
        self.recipe.title = 'Um valor qualquer' * 165
        
        with self.assertRaises(ValidationError):
            self.recipe.full_clean() # Aqui ocorre uma validação

    @parameterized.expand([
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    # def test_recipe_string_representation(self):
    #     needed = 'Testing Representation'
    #     self.recipe.title = needed
    #     self.recipe.full_clean()
    #     self.recipe.save()
    #     self.assertEqual(
    #         str(self.recipe), needed,
    #         msg=f'Recipe string representation must be '
    #             f'"{needed}" but "{str(self.recipe)}" was received.'
    #     )

    # def test_recipe_preparation_steps_is_html_is_false_by_default(self):
    #     recipe = self.make_recipe_no_defaults()
    #     self.assertFalse(
    #         recipe.preparation_steps_is_html,
    #         msg='Recipe preparation_steps_is_html is not False',
    #     )

    # def test_recipe_is_published_is_false_by_default(self):
    #     recipe = self.make_recipe_no_defaults()
    #     self.assertFalse(
    #         recipe.is_published,
    #         msg='Recipe is_published is not False',
    #     )