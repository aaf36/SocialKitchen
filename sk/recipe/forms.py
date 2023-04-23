from django import forms
from .models import Recipe, Ingredient, Category, RecipeIngredient
from django.forms import inlineformset_factory


class RecipeIngredientForm(forms.ModelForm):
    UNIT_CHOICES = (
        ('g', 'g'),
        ('ml', 'ml'),
        ('tbsp', 'tbsp'),
    )

    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    weight = forms.FloatField(min_value=0, initial=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    unit = forms.ChoiceField(choices=UNIT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'weight', 'unit']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'time_to_cook', 'description', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'time_to_cook': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        recipe = super().save(commit=commit)
        return recipe


