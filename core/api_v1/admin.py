from django.contrib import admin
from .models import Categories, Tags, News


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category_name']
    list_display_links = ['pk', 'category_name']
    ordering = ['pk']
    prepopulated_fields = {'category_slug': ['category_name']}


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'tag_name']
    list_display_links = ['pk', 'tag_name']
    ordering = ['pk']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'rating', 'created_datetime', 'updated_datetime']
    list_display_links = ['pk', 'title']
    ordering = ['pk']
    search_fields = ['title']

    list_filter = ['category__category_name', 'tags_new__tag_name']
    list_per_page = 5
    filter_horizontal = ['tags_new']

