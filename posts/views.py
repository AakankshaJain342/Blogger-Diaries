from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from blogs.models import Post
# from django import forms
# from datetime import datetime

# Create your views here.
def post_view(request, post_id):
  post = Post.objects.get(pk=post_id)
  return render(request, 'post_view.html', {'post': post})
