from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.home, name="recipes-home"),
    path('recipes/category/<int:category_id>/', views.category, name="recipes-category"),
    path('recipes/<int:id>/', views.recipe, name="recipes-recipe")

]