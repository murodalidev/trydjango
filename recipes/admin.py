from django.contrib import admin

from .models import Recipe, Ingredient


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInlineAdmin,)
    list_display = ('id', 'title', 'ingredients_count', 'author', 'created_date')
    list_display_links = ('title', 'id')
    filter_horizontal = ('tags',)
    search_fields = ('title', 'author__username')
    list_filter = ('created_date',)
    date_hierarchy = 'created_date'
    list_per_page = 25

    def ingredients_count(self, obj):
        return obj.ingredients.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'recipe', 'quantity', 'unit')
    search_fields = ('title', 'recipe__title')
    autocomplete_fields = ('recipe',)
