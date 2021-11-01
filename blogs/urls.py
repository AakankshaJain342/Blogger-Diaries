from django.urls import path
from .views import * 

app_name="blogs"

urlpatterns = [
  path('', index, name='index'),
  path('<int:blog_id>/', blog_view, name='blog_view'),
  path('new/', blog_create, name='blog_create'),
]