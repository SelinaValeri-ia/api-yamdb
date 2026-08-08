from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

router = DefaultRouter()

router.register(
    'categories',
    CategoryViewSet,
    basename='categories',
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres',
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles',
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'titles/<int:title_id>/reviews/',
        ReviewViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='review-list',
    ),
    path(
        'titles/<int:title_id>/reviews/<int:pk>/',
        ReviewViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='review-detail',
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/',
        CommentViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }),
        name='comment-list',
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/',
        CommentViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy',
        }),
        name='comment-detail',
    ),
]
