from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .forms import RecipeIngredientForm, RecipeForm
from .models import Recipe, RecipeIngredient


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse('user:login'))
    else:
        messages.success(request, "Welcome Back!")
        return render(request, "recipe/home.html")
    

def add_recipe(request):
    if not request.user.is_authenticated:
        return redirect(reverse('user:login'))
    else:
        if request.method == 'POST':
            recipe_form = RecipeForm(request.POST, request.FILES)
            recipe_ingredient_form = RecipeIngredientForm(request.POST)
            if recipe_form.is_valid() and recipe_ingredient_form.is_valid():
                recipe = recipe_form.save()
                recipe_ingredient = recipe_ingredient_form.save(commit=False)
                recipe_ingredient.recipe = recipe
                recipe_ingredient.save()
                return HttpResponse("success")
        else:
            recipe_form = RecipeForm()
            recipe_ingredient_form = RecipeIngredientForm()
        return render(request, 'recipe/add_recipe.html', {'recipe_form': recipe_form, 'ingredient_form': recipe_ingredient_form})






