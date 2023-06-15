from django.contrib import admin
from .models import Article, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')



class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'slug', 'category', "modified_date", "created_date")
    fields = ("title", 'slug', 'category', "image", "body", 'tags', "modified_date", "created_date")
    readonly_fields = ("modified_date", "created_date")
    # prepopulated_fields = {"slug": ("title", )}
    search_fields = ("title", )
    filter_horizontal = ('tags', )
    list_filter = ("created_date", 'category')
    list_editable = ('category', )



admin.site.register(Article, ArticleAdmin)

