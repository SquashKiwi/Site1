from django.shortcuts import render
from rest_framework.decorators import api_view



@api_view(['GET'])
def get_home(request):
    return render(request, 'main_home.html')