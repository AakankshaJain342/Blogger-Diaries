from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from blogs.models import Post
from django import forms
from markdown import markdown
# from django import forms
# from datetime import datetime

class PostEditForm(forms.ModelForm):
  title = forms.CharField(max_length=40, label="Title", required=True,widget=forms.TextInput(attrs={'class': "form-control"}))
  body = forms.CharField(label='Body',required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
  class Meta:
    model = Post
    fields = ['title', 'body']

# Create your views here.
def post_view(request, post_id):
  post = Post.objects.get(pk=post_id)
  post_html = markdown(post.body)
  return render(request, 'post_view.html', {'post': post, 'post_html': post_html})

@login_required(login_url=reverse_lazy('auth:login'))
def post_edit(request,post_id):
  # Check if user is the owner of the blog.
  post=Post.objects.get(id=post_id)
  # print('hi',post.blog.user,request.user,request.method);
  if(post.blog.user!=request.user):
    messages.add_message(request, messages.ERROR, "You do not have the permission to edit this blog.")
    return redirect('posts:post_view',post_id=post_id)
  
  if request.method == 'POST':
    form = PostEditForm(request.POST,initial={'title': 'Aakanksha'})
    if form.is_valid():
      post_data = form.save(commit=False)
      try:
        post.title = post_data.title
        post.body = post_data.body
        # print(post_data)
        post.save()
      except:
        return render(request, 'post_edit.html', {'form': form, 'post': post})
      return redirect('posts:post_view',post_id=post_id)
    return render(request, 'post_edit.html', {'form': form, 'post': post})
  else:
    form = PostEditForm({'title': post.title, 'body': post.body})
    return render(request, 'post_edit.html', {'form': form, 'post': post})