from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Todo.objects.all()
        user_id = self.request.query_params.get('user')
        if user_id:
            return queryset.filter(user_id=user_id)
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)