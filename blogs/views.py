from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from blogs.models import Blog, Post
from django import forms
from datetime import datetime

class BlogCreationForm(forms.ModelForm):
  title = forms.CharField(max_length=30, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
  description = forms.CharField(max_length=500, label='Description',required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
  class Meta:
    model = Blog
    fields = ['title', 'description']

class BlogEditForm(forms.ModelForm):
  title = forms.CharField(max_length=40, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
  description = forms.CharField(max_length=500, label='Description',required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
  class Meta:
    model = Blog
    fields = ['title', 'description']

class PostCreationForm(forms.ModelForm):
  title = forms.CharField(max_length=40, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
  body = forms.CharField(label='Body',required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
  class Meta:
    model = Post
    fields = ['title', 'body']

# Create your views here.
def index(request):
  blogs = Blog.objects.all()
  print(blogs)
  return render(request, 'index.html', {'blogs': blogs})

def blog_view(request, blog_id):
  blog = Blog.objects.get(pk=blog_id)
  return render(request, 'blog_view.html', {'blog': blog})

@login_required(login_url=reverse_lazy('auth:login'))
def blog_create(request):
  if request.method == 'POST':
    form = BlogCreationForm(request.POST)
    if form.is_valid():
      blog = form.save(commit=False)
      blog.date = datetime.now()
      blog.user = request.user
      blog.save()
      return render(request, 'blog_view.html', {'blog': blog})
    return render(request, 'blog_create.html', {'form': form})
  else:
    form = BlogCreationForm()
    return render(request, 'blog_create.html', {'form': form})

@login_required(login_url=reverse_lazy('auth:login'))
def blog_edit(request,blog_id):
  # Check if user is the owner of the blog.
  blogedit=Blog.objects.get(id=blog_id)
  if(blogedit.user!=request.user):
    messages.add_message(request, messages.ERROR, "You do not have the permissions to edit this blog.")
    return redirect('blogs:blog_view',blog_id=blog_id)
  
  if request.method == 'POST':
    form = BlogEditForm(request.POST,initial={'title': 'Aakanksha'})
    if form.is_valid():
      blog = form.save(commit=False)
      try:
        blogedit.title = blog.title
        blogedit.description = blog.description
        blogedit.save()
      except:
        return render(request, 'blog_edit.html', {'form': form})
      # blog.date = datetime.now()
      # blog.user = request.user
      # blog.save()
      print(blog.title)
      return render(request, 'blog_view.html', {'blog': blog})
    return render(request, 'blog_edit.html', {'form': form})
  else:
    form = BlogEditForm()
    return render(request, 'blog_edit.html', {'form': form, 'blog': blogedit})

@login_required(login_url=reverse_lazy('auth:login'))
def post_create(request, blog_id):
  blog=Blog.objects.get(id=blog_id)
  if(blog.user!=request.user):
    messages.add_message(request, messages.ERROR, "You do not have the permissions to edit this blog.")
    return redirect('blogs:blog_view',blog_id=blog_id)

  if request.method == 'POST':
    form = PostCreationForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.date = datetime.now()
      post.blog = blog
      post.save()
      return render(request, 'post_view.html', {'post': post})
    return render(request, 'post_create.html', {'form': form})
  else:
    form = PostCreationForm()
    return render(request, 'post_create.html', {'form': form})
