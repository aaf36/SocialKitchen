from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
from django.urls import reverse

from macros.models import RecipeIngredientMacros, RecipeMacros
from .forms import RecipeIngredientForm, RecipeForm
from .models import Recipe, RecipeIngredient
from macros.views import calc_macros, convert2grams


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        recipes = Recipe.objects.all
        return render(request, "recipe/home.html", {'recipes':recipes})
    

def add_recipe(request):
    if not request.user.is_authenticated:
        messages.success(request, "You need to login before accessing this page.")
        return redirect(reverse('user:login'))
    else:
        RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
        if request.method == 'POST':
            form = RecipeForm(request.POST, request.FILES)
            formset = RecipeIngredientFormset(request.POST, queryset=RecipeIngredient.objects.none())
            if all([form.is_valid(), formset.is_valid()]):
                recipe = form.save()
                ingredients = formset.save(commit=False)
                total_calories = 0
                total_protein = 0
                total_carbs = 0
                total_fats = 0
                for ingredient in ingredients:
                    ingredient.recipe = recipe
                    ingredient.save()
                    ingredient_macros = RecipeIngredientMacros()
                    ingredient_macros.recipe_ingredient = ingredient
                    ingredient_macros.calories = calc_macros(ingredient.ingredient.calories, convert2grams(ingredient.unit, ingredient.quantity))
                    ingredient_macros.protein = calc_macros(ingredient.ingredient.protein, convert2grams(ingredient.unit, ingredient.quantity))
                    ingredient_macros.carbs = calc_macros(ingredient.ingredient.carbs, convert2grams(ingredient.unit, ingredient.quantity))
                    ingredient_macros.fats = calc_macros(ingredient.ingredient.fats, convert2grams(ingredient.unit, ingredient.quantity))
                    ingredient_macros.save()
                    total_calories += ingredient_macros.calories
                    total_protein += ingredient_macros.protein
                    total_carbs += ingredient_macros.carbs
                    total_fats += ingredient_macros.fats
                recipe_macros = RecipeMacros()
                recipe_macros.recipe = recipe
                recipe_macros.calories = total_calories
                recipe_macros.protein = total_protein
                recipe_macros.carbs = total_carbs
                recipe_macros.fats = total_fats
                recipe_macros.save()
                return render(request, "recipe/details_recipe.html", {'recipe':recipe,'ingredients':ingredients, 'macros':recipe_macros})
        else:
            form = RecipeForm()
            formset = RecipeIngredientFormset(queryset=RecipeIngredient.objects.none())
        return render(request, 'recipe/add_recipe.html', {'form':form, 'formset': formset})


def details(request, id):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        recipe = get_object_or_404(Recipe, pk=id)
        ingredients = recipe.recipeingredient_set.all()
        return render(request, "recipe/details_recipe.html", {'recipe':recipe, 'ingredients':ingredients})


def remove_recipe(request,id):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        recipe = get_object_or_404(Recipe, pk=id)
        recipe.delete()
        messages.success(request, "Recipe Have Been Removed Successfully")
        return redirect(reverse('recipe:home'))


def update_recipe(request, id):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        recipe = get_object_or_404(Recipe, pk=id)
        RecipeIngredientFormset = modelformset_factory(
            RecipeIngredient, 
            form=RecipeIngredientForm, 
            extra=0
        )

        if request.method == 'POST':
            form = RecipeForm(request.POST, request.FILES, instance=recipe)
            formset = RecipeIngredientFormset(request.POST, queryset=recipe.recipeingredient_set.all())

            if form.is_valid() and formset.is_valid():
                recipe = form.save()
                for ingredient_form in formset:
                    if ingredient_form.is_valid():
                        ingredient = ingredient_form.save(commit=False)
                        ingredient.recipe = recipe
                        ingredient.save()

                messages.success(request, "Recipe updated successfully!")
                return redirect(reverse('recipe:details', args=[recipe.pk]))

        else:
            form = RecipeForm(instance=recipe)
            formset = RecipeIngredientFormset(queryset=recipe.recipeingredient_set.all())
            formset.prefix = 'form'

        return render(request, 'recipe/update_recipe.html', {'form': form, 'formset': formset, 'recipe': recipe})

def search_recipe(request):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        results= []
        if request.method== "POST":
            search_query = request.POST.get('search')
            recipes = Recipe.objects.all()
            for recipe in recipes:
                if search_query.lower() == recipe.name.lower():
                    results.append(recipe)
                    break
                else:
                    if search_query.lower() in recipe.name.lower():
                        results.append(recipe)

            return render(request, "recipe/search_recipe.html", {'results':results})
