from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.template import loader


@api_view(['GET'])
def myapp_link(request):
    response = requests.get("http://127.0.0.1:8000/api/item/create_r/")
    return render(request, 'done.html', response.json())