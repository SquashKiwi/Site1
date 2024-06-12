# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .serializers import HelloSerializer

@api_view(['GET'])
def hello_django(request):
    return Response({"message": "Hello Django"})
    # return HttpResponse("Hello")
    

@api_view(['POST'])
def hello_post(request):
    serializer = HelloSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data.get('name')
        return Response({"message": f"Hello {name}"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

