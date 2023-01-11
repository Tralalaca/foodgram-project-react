import django_filters as filters
from django_filters.rest_framework import FilterSet

from .models import Ingredient, Recipe, Tag


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                             queryset=Tag.objects.all(),)
    is_favorited = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(), label='В избранных.')
    is_in_shopping_cart = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(), label='В корзине.')

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)
