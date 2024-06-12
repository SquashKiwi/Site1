# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_django(request):
    return Response({"message": "Hello Django"})
