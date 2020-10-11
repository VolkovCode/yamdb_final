from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet, UsersViewSet, UserMeViewSet,
    ReviewViewSet, CommentViewSet, get_confirmation_code, get_token, refresh_token
)


v1_router = DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/users/me/', UserMeViewSet.as_view(), name='me'),
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', get_confirmation_code, name='get_confirmation_code'),
    path('v1/token/', get_token, name='get_token'),
    path('v1/token/refresh/', refresh_token, name='refresh_token'),
]
