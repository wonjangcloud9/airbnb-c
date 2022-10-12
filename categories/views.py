from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Category
from .serializers import CategorySerializer

# Create your views here.


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(
            serializer.data,
        )
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        return Response(serializer.errors)


@api_view(["GET", "PUT"])
def category(request, pk):
    if request.method == "GET":
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(
                serializer.data,
            )
        except Category.DoesNotExist:
            return Response(
                {
                    "error": "Category not found",
                },
                status=404,
            )
    elif request.method == "PUT":
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                updated_category = serializer.save()
                return Response(CategorySerializer(updated_category).data)
            return Response(serializer.errors)
        except Category.DoesNotExist:
            return Response(
                {
                    "error": "Category not found",
                },
                status=404,
            )
