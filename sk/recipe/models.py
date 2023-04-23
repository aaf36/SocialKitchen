from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField(default=100, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=4, default='g')
    brand = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'brand'], name='unique_ingredient')
        ]

    def __str__(self):
        return f'{self.name} ({self.brand})' if self.brand else self.name

class Recipe(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    time_to_cook = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField('Ingredient', related_name='recipes', through='RecipeIngredient')

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.FloatField(default=0, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=4, default='g')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_recipe_ingredient')
        ]

    def __str__(self):
        return f'{self.ingredient.name} - {self.recipe.name} - {self.weight}{self.unit}'



