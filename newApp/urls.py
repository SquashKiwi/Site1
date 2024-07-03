from django.urls import path
from .views import myapp_link


urlpatterns = [
    path("", myapp_link)

]