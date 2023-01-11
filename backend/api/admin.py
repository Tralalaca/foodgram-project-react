from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Recipe)
class AdminRecupes(admin.ModelAdmin):
    list_display = ('author', 'name', 'image', 'text', 'cooking_time',
                    'cooking_time', 'pub_date')


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


@admin.register(RecipeIngredient)
class AdminRecipeIngredient(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
