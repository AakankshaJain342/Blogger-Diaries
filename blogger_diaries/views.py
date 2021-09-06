from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.

def home_view(request):
  return render(request, "home.html")