from core.views import BaseModelViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from .models import Post
from .serializers import PostSerializer

class IsOwnerOrReadOnly(BasePermission):
    """
    Sadece postun sahibi (author) silebilir veya güncelleyebilir.
    Diğer kullanıcılar sadece okuyabilir (GET).
    """
    def has_object_permission(self, request, view, obj):
        # Okuma istekleri (GET, HEAD, OPTIONS) herkese serbest
        if request.method in SAFE_METHODS:
            return True

        # Silme veya güncelleme için postun sahibi ile giriş yapan kullanıcı aynı olmalı
        return obj.author == request.user

class PostViewSet(BaseModelViewSet):
    serializer_class = PostSerializer
    # Burada hem giriş yapmış olma şartını hem de sadece sahibinin silebilmesi kuralını bağlıyoruz
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        author_id = self.request.query_params.get('author')
        if author_id:
            return queryset.filter(author_id=author_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)