from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AddDeleteFavoriteRecipe, AddDeleteShoppingCart,
                    IngredientsViewSet, RecipesViewSet, TagsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/favorite/',
         AddDeleteFavoriteRecipe.as_view(),
         name='favorite_recipe'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         AddDeleteShoppingCart.as_view(),
         name='shopping_cart'),
]
