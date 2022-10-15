from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer

# Create your views here.


class categoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
