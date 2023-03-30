from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name="recipes-home"),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name="recipes-search"),
    path('recipes/tags/<slug:slug>/', views.RecipeListViewTag.as_view(), name="recipes-tags"),
    path('recipes/category/<int:pk>/', views.RecipeListViewCategory.as_view(), name="recipes-category"),
    # path('recipes/<int:id>/', views.recipe, name="recipes-recipe"),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name="recipes-recipe"),
    path('recipes/api/v1/', views.RecipeListViewHomeAPI.as_view(), name=''),
    path('recipes/api/v1/<int:pk>/', views.RecipeDatailViewPI.as_view(), name=''),
]