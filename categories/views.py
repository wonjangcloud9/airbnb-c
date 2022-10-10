from django.http import JsonResponse
from .models import Category

# Create your views here.


def categories(request):
    categories = Category.objects.all()
    return JsonResponse({"categories": list(categories.values())})
