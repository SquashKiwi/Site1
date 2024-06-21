# myapp/urls.py
from django.urls import path
from .views import hello_django, hello_post, hello_patch, hello_delete, upload_image
from .views import register, CustomAuthToken, post_item, get_item, update_item, delete_item
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # path('admin/', admin.site.urls)
    path('hello/', hello_django),
    path('hello_post/', hello_post),
    path('hello_patch/<int:pk>/', hello_patch),
    path('hello_delete/<int:pk>/', hello_delete),
    path('upload_image/', upload_image),
    path('register/', register),
    path('login/', CustomAuthToken.as_view()),
    path('item/', get_item),
    path('item/save', post_item),
    path('item/delete/<int:pk>/', delete_item),
    path('item/update/<int:pk>/', update_item),

]
