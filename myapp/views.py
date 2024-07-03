import json
# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status, viewsets
from .serializers import MessageSerializer, ImageUploadSerializer, UserSerializer, ItemSerializer
from .models import Message, Item
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.db import connection

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from myapp.models import Item
from django.views.decorators.csrf import csrf_exempt

# JWT
import jwt 
SECRET_KEY = "secretkey"

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


def validate_image_format(image):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/jpg']
    if image.content_type not in valid_mime_types:
        raise ValidationError("incorrect format")

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def upload_image(request):
    auth_token = str(request.META["HTTP_AUTHORIZATION"]).split()[1] # token
    print(auth_token)
    decoded = jwt.decode(auth_token.strip(), SECRET_KEY, algorithms=["HS256"])
    print(decoded)
    # print(f"USER: {current_user}")
    if str(decoded) != "{'user': 'testuser16'}":
        return Response({"error": "invalid authentication token"}, status=status.HTTP_400_BAD_REQUEST)
    if 'image' not in request.FILES:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

    image = request.FILES['image']

    try:
        validate_image_format(image)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ImageUploadSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        global current_user 
        current_user += str(user)
        # print("USer data", user)
        jwt_token = jwt.encode({"user": str(user)}, SECRET_KEY, algorithm="HS256")
        return Response({'token': jwt_token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token})
    


# @permission_classes([AllowAny])
@api_view(['GET'])
def get_item(request):
    items = Item.objects.all()
    

    list_items = [[item.name, item.description] for item in items]   
    serializer = ItemSerializer(items, many=True)
    return render(request, 'show_item.html', {'item': serializer.data})

@api_view(['POST'])
def post_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_item(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# @permission_classes([AllowAny])

@api_view(['POST', 'GET'])
@csrf_exempt
def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'GET':
        return render(request, 'update_item.html', {'item': item, 'pk': pk})
    
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            name = data.get('name')
            description = data.get('description')

            if not name or not description:
                return JsonResponse({'error': 'Invalid input'}, status=400)

            item.name = name
            item.description = description
            item.save()

            return JsonResponse({'message': 'Item updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only GET and PUT methods allowed'}, status=405)
    


@api_view(['GET', 'POST'])
@csrf_exempt
def home(request):
    try:
        items = Item.objects.all()
        count = items.count()
        
    except:
        return JsonResponse({'error': 'Could not access DB'}, status=400)

    return render(request, 'home_page.html', {'count':count})


@api_view(['GET', 'POST'])
@csrf_exempt
def delete_last(request):
    try:
        items = Item.objects.all()
        item  = items.get(pk=items[items.count()-1].id)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    item.delete()
    count = items.count()
    return render(request, 'home_page.html', {'count': count})


@api_view(['GET', 'POST'])
@csrf_exempt
def create_random(request):
    serializer = ItemSerializer(data= {'name':'New name',
                                       'description' : 'Description',})
    status = 'Incomplete'
    if serializer.is_valid():
        serializer.save()
        status = 'Complete'

    try:
        items = Item.objects.all()
        count = items.count()
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({'count' : count , 'status' : status})

