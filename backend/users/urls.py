from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddAndDeleteSubscribe, AuthToken, UsersViewSet, set_password

router = DefaultRouter()
router.register('users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/login/', AuthToken.as_view(), name='login'),
    path('users/set_password/', set_password, name='set_password'),
    path('users/<int:user_id>/subscribe/',
         AddAndDeleteSubscribe.as_view(), name='subscribe'),
]
