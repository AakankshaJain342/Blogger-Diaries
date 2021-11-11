from django.urls import path
from .views import * 

app_name="posts"

urlpatterns = [
  # path('', index, name='index'),
  path('<int:post_id>/', post_view, name='post_view'),
  path('<int:post_id>/edit/', post_edit, name="post_edit"),
]