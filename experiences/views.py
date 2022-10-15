from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Perk
from .serializers import PerkSerializer


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(status=404)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            return Response(status=404)

    def get(self, request, pk):
        try:
            perk = Perk.objects.get(pk=pk)
            serializer = PerkSerializer(perk)
            return Response(data=serializer.data)
        except Perk.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(status=404)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=204)
