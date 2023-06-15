from django.urls import path
from .views import recipes_list, recipe_create, recipe_detail, recipe_edit, recipe_delete,\
    ingredient_create, ingredient_edit, ingredient_delete


app_name = 'recipes'

urlpatterns = [
    path('', recipes_list, name='list'),
    path('create/', recipe_create, name='create'),
    path('detail/<int:pk>/', recipe_detail, name='detail'),
    path('edit/<int:pk>/', recipe_edit, name='edit'),
    path('delete/<int:pk>/', recipe_delete, name='delete'),

    path('<int:recipe_id>/ingredienet/create/', ingredient_create, name='ing_create'),
    path('<int:recipe_id>/ingredienet/edit/<int:pk>/', ingredient_edit, name='ing_edit'),
    path('<int:recipe_id>/ingredienet/delete/<int:pk>/', ingredient_delete, name='ing_delete'),
]
