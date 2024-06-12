# myapp/serializers.py
from rest_framework import serializers
from .models import Message

class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']