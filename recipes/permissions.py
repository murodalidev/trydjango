from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from recipes.models import Recipe, Ingredient


def is_owner_to_recipe_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        obj = get_object_or_404(Recipe, id=kwargs['pk'])
        if obj.author != request.user:
            return HttpResponseForbidden("You are not the owner of this object.")
        return view_func(request, *args, **kwargs)
    return wrapper


def is_owner_to_ing_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        obj = get_object_or_404(Ingredient, id=kwargs['pk'])
        if obj.recipe.author != request.user:
            return HttpResponseForbidden("You are not the owner of this object.")
        return view_func(request, *args, **kwargs)
    return wrapper

