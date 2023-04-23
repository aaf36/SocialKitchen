from django.urls import path
from . import views


app_name= "recipe"

urlpatterns= [
    path('home/', views.home, name="home"),
    path('add_recipe/', views.add_recipe, name="add-recipe")
]