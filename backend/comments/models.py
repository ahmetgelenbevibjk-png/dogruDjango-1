from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models
from posts.models import Post

User = get_user_model()


class Comment(BaseModel):
  post = models.ForeignKey(
      Post, on_delete=models.CASCADE, related_name='comments'
  )
  user = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name='comments'
  )
  content = models.TextField()
  # Hangi yoruma yanıt verildiğini tutar (Ana yorumsa boş/null olur)
  parent = models.ForeignKey(
      'self',
      null=True,
      blank=True,
      on_delete=models.CASCADE,
      related_name='replies',
  )
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.user.username} - {self.content[:30]}'