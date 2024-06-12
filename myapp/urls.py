# myapp/urls.py
from django.urls import path
from .views import hello_django, hello_post, hello_patch, hello_delete

urlpatterns = [
    path('hello/', hello_django),
    path('hello_post/', hello_post),
    path('hello_patch/<int:pk>/', hello_patch),
    path('hello_delete/<int:pk>/', hello_delete),
]
