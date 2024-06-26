from django.contrib import admin
from .models import Message, ImageUpload, Item

# Register your models here.
admin.site.register(Message)
admin.site.register(ImageUpload)
admin.site.register(Item)