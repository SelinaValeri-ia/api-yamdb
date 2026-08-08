from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, signup, token_obtain

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', token_obtain),
    path('', include(router_v1.urls)),
]
