import io
from os import path

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from django.db.models.expressions import Exists, OuterRef, Value
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, TagSerializer)
from .utils import DataMixin, PermissionsMixin

User = get_user_model()


class AddDeleteFavoriteRecipe(DataMixin,
                              generics.RetrieveDestroyAPIView,
                              generics.ListCreateAPIView):

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        request.user.favorite_recipe.recipe.add(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        self.request.user.favorite_recipe.recipe.remove(instance)


class AddDeleteShoppingCart(DataMixin,
                            generics.RetrieveDestroyAPIView,
                            generics.ListCreateAPIView):

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        request.user.shopping_cart.recipe.add(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        self.request.user.shopping_cart.recipe.remove(instance)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        return Recipe.objects.annotate(
            is_favorited=Exists(
                FavoriteRecipe.objects.filter(
                    user=self.request.user, recipe=OuterRef('id'))),
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(
                    user=self.request.user,
                    recipe=OuterRef('id')))
        ).select_related('author').prefetch_related(
            'tags', 'ingredients', 'recipe',
            'shopping_cart', 'favorite_recipe'
        ) if self.request.user.is_authenticated else Recipe.objects.annotate(
            is_in_shopping_cart=Value(False),
            is_favorited=Value(False),
        ).select_related('author').prefetch_related(
            'tags', 'ingredients', 'recipe',
            'shopping_cart', 'favorite_recipe')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_card = (
            request.user.shopping_cart.recipe.values(
                'ingredients__name',
                'ingredients__measurement_unit'
            ).annotate(amount=Sum('recipe__amount')).order_by())

        shopping_list = ''
        shopping_list += '\n'.join([
            f'- {card_item["ingredients__name"]} '
            f'({card_item["ingredients__measurement_unit"]})'
            f' - {card_item["amount"]}'
            for card_item in shopping_card
        ])

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=shopping_list.txt'
        return response

class TagsViewSet(PermissionsMixin,
                  viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(PermissionsMixin,
                         viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
