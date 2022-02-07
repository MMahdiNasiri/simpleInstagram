from django.db import models
from django.contrib.auth.models import User
# from PIL import Image


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments')
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="posts")
    content = models.TextField(blank=True, null=True)
    # image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
