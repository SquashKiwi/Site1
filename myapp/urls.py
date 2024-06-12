# myapp/urls.py
from django.urls import path
from .views import hello_django, hello_post

urlpatterns = [
    path('hello/', hello_django),
    path('hello_post/', hello_post),
]
