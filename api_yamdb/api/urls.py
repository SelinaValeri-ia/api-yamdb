from django.urls import path

from .views import token_obtain

urlpatterns = [
    path('auth/token/', token_obtain),
]
