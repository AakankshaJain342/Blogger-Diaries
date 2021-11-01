from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=30)
  description = models.TextField()
  date = models.DateField()
  followers = models.ManyToManyField(User, related_name="followers")

class Post(models.Model):
  body = models.TextField()
  title = models.CharField(max_length=30)
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")
  date = models.DateField()

class Comment(models.Model):
  text = models.TextField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
  date = models.DateField(null=True)

