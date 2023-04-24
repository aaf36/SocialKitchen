from django.forms import modelformset_factory
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.urls import reverse
from .forms import RecipeIngredientForm, RecipeForm
from .models import Recipe, RecipeIngredient


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        messages.success(request, "Cannot Access Page Please Login...")
        return redirect(reverse('user:login'))
    else:
        return render(request, "recipe/home.html")
    

def add_recipe(request):
    if not request.user.is_authenticated:
        messages.success(request, "Cannot Access Page Please Login...")
        return redirect(reverse('user:login'))
    else:
        RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=3)
        if request.method == 'POST':
            form =RecipeForm(request.POST, request.FILES)
            formset = RecipeIngredientFormset(request.POST, queryset=RecipeIngredient.objects.none())
            if all([form.is_valid(), formset.is_valid()]):
                recipe= form.save()
                ingredients = formset.save(commit=False)
                for ingredient in ingredients:
                    ingredient.recipe= recipe
                    ingredient.save()
                return HttpResponse("success")
                
        else:
            form = RecipeForm()
            formset = RecipeIngredientFormset(queryset=RecipeIngredient.objects.none())
        return render(request, 'recipe/add_recipe.html', {'form':form, 'formset': formset})






