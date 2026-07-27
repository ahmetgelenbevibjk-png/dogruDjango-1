from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.all()
        author_id = self.request.query_params.get('author')
        if author_id:
            return queryset.filter(author_id=author_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)