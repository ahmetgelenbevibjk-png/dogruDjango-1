from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, AlbumImageViewSet

router = DefaultRouter()
router.register(r'albums', AlbumViewSet)
router.register(r'album-images', AlbumImageViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
