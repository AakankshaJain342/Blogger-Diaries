from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from blogs.models import Blog
from django import forms
from datetime import datetime

class BlogCreationForm(forms.ModelForm):
  title = forms.CharField(max_length=40, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
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
  if request.method == 'POST':
    form = BlogEditForm(request.POST,initial={'title': 'Aakanksha'})
    if form.is_valid():
      blog = form.save(commit=False)
      try:
        blogedit=Blog.objects.get(id=blog_id)
        if(blogedit.user!=request.user):
          return render(request, 'blog_edit.html', {'form': form})
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
    blogedit=Blog.objects.get(id=blog_id)
    return render(request, 'blog_edit.html', {'form': form, 'blog': blogedit})
       