from django.contrib import admin
from .models import Message, ImageUpload

# Register your models here.
admin.site.register(Message)
admin.site.register(ImageUpload)