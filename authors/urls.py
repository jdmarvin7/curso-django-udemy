from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_view_create, name='login_create'),
    path('logout/', views.login_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/recipe/delete/',
        views.dashboard_recipe_delete,
        name='dashboard_recipe_delete'
    ),
    path(
        'dashboard/recipe/<int:id>/edit/',
        views.dashboard_recipe_edit,
        name='dashboard_recipe_edit'
    ),
    path('create-recipe/', views.create_recipe, name='create_recipe')
]