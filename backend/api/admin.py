from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)
    min_num = 1


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):

    list_display = ('author', 'image', 'text', 'cooking_time',
                    'cooking_time', 'pub_date', 'get_ingredients')

    inlines = (RecipeIngredientInline,)

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return '\n '.join([
            f'{item["ingredient__name"]} - {item["amount"]}'
            f' {item["ingredient__measurement_unit"]}.'
            for item in obj.recipe.values(
                'ingredient__name',
                'amount', 'ingredient__measurement_unit')])


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


@admin.register(RecipeIngredient)
class AdminRecipeIngredient(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
