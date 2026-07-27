from rest_framework import serializers
from .models import Post
from comments.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username', default='Anonim')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_name', 'title', 'body', 'comments', 'created_at']
        read_only_fields = ['author']
