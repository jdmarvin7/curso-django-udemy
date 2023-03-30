from django.apps import AppConfig


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'

    def ready(self) -> None:
        import recipes.signals
        super_ready = super().ready()
        return super_ready
