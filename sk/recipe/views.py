from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .forms import RecipeIngredientForm, RecipeForm
from .models import Recipe, RecipeIngredient


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        return render(request, "recipe/home.html")
    

def add_recipe(request):
    if not request.user.is_authenticated:
        messages.success(request, "You Need To Login Before Accessing This Page...")
        return redirect(reverse('user:login'))
    else:
        RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=1)
        if request.method == 'POST':
            form =RecipeForm(request.POST, request.FILES)
            formset = RecipeIngredientFormset(request.POST, queryset=RecipeIngredient.objects.none())
            if all([form.is_valid(), formset.is_valid()]):
                recipe= form.save()
                ingredients = formset.save(commit=False)
                for ingredient in ingredients:
                    ingredient.recipe = recipe
                    ingredient.save()
                return render(request, "recipe/details_recipe.html", {'recipe':recipe,'ingredients':ingredients})
                
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


