from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, UserListView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('all-users/', UserListView.as_view(), name='user-list'),
] + router.urls
