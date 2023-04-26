from django.urls import path
from . import views


app_name= "recipe"

urlpatterns= [
    path('home/', views.home, name="home"),
    path('add/', views.add_recipe, name="add-recipe"),
    path('details/<int:id>/', views.details, name="details"),
    path('remove/<int:id>/', views.remove_recipe, name="remove-recipe"),
    path('update/<int:id>/', views.update_recipe, name="update-recipe"),
    path('search/', views.search_recipe, name="search-recipe")
]