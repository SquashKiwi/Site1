# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import HttpResponse
from rest_framework import status
from .serializers import HelloSerializer, MessageSerializer
from .models import Message
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def hello_django(request):
    return Response({"message": "Hello Django"})
    # return HttpResponse("Hello")
    

@api_view(['POST'])
def hello_post(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def hello_patch(request, pk):
    message = get_object_or_404(Message, pk=pk)
    serializer = MessageSerializer(message, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def hello_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


