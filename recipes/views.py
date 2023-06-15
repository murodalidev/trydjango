from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .models import Recipe, Ingredient, Tag
from .forms import RecipeForm, IngredientForm
from .permissions import is_owner_to_recipe_decorator, is_owner_to_ing_decorator


def recipes_list(request):
    recipes = Recipe.objects.order_by('-id')
    tags = Tag.objects.all()
    tag = request.GET.get('tag')
    if tag:
        recipes = recipes.filter(tags__title__exact=tag)

    ctx = {
        'object_list': recipes,
        'tags': tags,
    }
    return render(request, 'recipes/list.html', ctx)


@login_required()
def recipe_create(request):
    # if not request.user.is_authenticated:
    #     next_path = request.path
    #     full_path = f"{reverse('accounts:login')}?next={next_path}"
    #     return redirect(full_path)
    form = RecipeForm(request.POST or None)
    user = request.user
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = user
        obj.save()
        form.save_m2m()
        return redirect('recipes:list')
    ctx = {
        'form': form
    }
    return render(request, 'recipes/create.html', ctx)


def recipe_detail(request, pk):
    obj = get_object_or_404(Recipe, id=pk)
    ctx = {
        'object': obj,
    }
    return render(request, 'recipes/detail.html', ctx)


@login_required()
@is_owner_to_recipe_decorator
def recipe_edit(request, pk):
    obj = get_object_or_404(Recipe, id=pk)
    form = RecipeForm(instance=obj)
    if request.method == 'POST':
        form = RecipeForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Recipe object "{obj.title}" is changed')
            return redirect(reverse('recipes:detail', kwargs={"pk": pk}))
    ctx = {
        'form': form
    }
    return render(request, 'recipes/edit.html', ctx)


@is_owner_to_recipe_decorator
def recipe_delete(request, pk):
    obj = get_object_or_404(Recipe, id=pk)
    model_meta = Recipe._meta
    related_fields = [
        {'name': field.name, 'objects': field.related_model.objects.filter(recipe=obj)}
        for field in model_meta.get_fields()
        if (field.one_to_many or field.one_to_one or field.many_to_many)
    ]

    if request.method == "POST":
        obj.delete()
        messages.error(request, f'Recipe object "{obj.title}" is deleted')
        return redirect('recipes:list')
    ctx = {
        'object': obj,
        'related_fields': related_fields,
    }
    return render(request, 'recipes/delete.html', ctx)


def ingredient_create(request, recipe_id):
    form = IngredientForm()
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.recipe_id = recipe_id
            obj.save()
            messages.success(request, f'Successfully added new ingredient {obj.title}')
            return redirect(reverse('recipes:detail', kwargs={"pk": recipe_id}))
    ctx = {
        'form': form,
        'recipe_id': recipe_id,
    }
    return render(request, 'recipes/ing/create.html', ctx)


@login_required
@is_owner_to_ing_decorator
def ingredient_edit(request, recipe_id, pk):
    obj = get_object_or_404(Ingredient, id=pk)
    form = IngredientForm(instance=obj)
    if request.method == 'POST':
        form = IngredientForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully change ingredint "{obj.title}"')
            return redirect(reverse('recipes:detail', kwargs={'pk': recipe_id}))
    ctx = {
        'object': obj,
        'form': form,
        'recipe_id': recipe_id
    }
    return render(request, 'recipes/ing/create.html', ctx)


@login_required
@is_owner_to_ing_decorator
def ingredient_delete(request, **kwargs):
    obj = get_object_or_404(Ingredient, id=kwargs.get('pk'))
    if request.method == 'POST':
        obj.delete()
        messages.error(request, f'Successfully deleted ingredient "{obj.title}"')
        return redirect(reverse('recipes:detail', kwargs={'pk': kwargs.get('recipe_id')}))
    ctx = {
        'object': obj,
        "url_kwargs": kwargs
    }
    return render(request, 'recipes/ing/delete.html', ctx)

