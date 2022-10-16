from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return NotFound


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            return Response(status=404)

    def get(self, request, pk):
        try:
            amenity = Amenity.objects.get(pk=pk)
            serializer = AmenitySerializer(amenity)
            return Response(data=serializer.data)
        except Amenity.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(status=404)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=204)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    return Response(status=400, data={"error": "Category is required"})
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        return Response(
                            status=400, data={"error": "Category is not for rooms"}
                        )
                except Category.DoesNotExist:
                    return Response(
                        status=400, data={"error": "Category is not for rooms"}
                    )
                room = serializer.save(owner=request.user, category=category)
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    try:
                        Amenity.objects.get(pk=amenity_pk)
                        room.amenity.add(amenity_pk)
                    except Amenity.DoesNotExist:
                        pass
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            else:
                return Response(status=400)


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=404)

    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = RoomDetailSerializer(room)
            return Response(data=serializer.data)
        except Room.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(status=404)

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()
        return Response(status=204)
