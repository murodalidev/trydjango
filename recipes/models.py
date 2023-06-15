from django.db import models
from django.contrib.auth.models import User
from articles.models import Tag


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=221)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_ingredients_count(self):
        return self.ingredients.count()

    def get_tags_count(self):
        return self.tags.count()

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    UNIT = (
        (0, "gram"),
        (1, "kilogram"),
        (2, "liter"),
        (3, "retail"),
        (4, "teaspoon"),
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    title = models.CharField(max_length=221)
    quantity = models.IntegerField()
    unit = models.IntegerField(choices=UNIT)

    def __str__(self):
        return self.title

