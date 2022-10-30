from django.conf import settings
from django.utils import timezone
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Review
from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


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

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms, many=True, context={"request": request}
        )
        return Response(data=serializer.data)

    def post(self, request):
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
                return Response(status=400, data={"error": "Category is not for rooms"})
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )

                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        Amenity.objects.get(pk=amenity_pk)
                        room.amenity.add(amenity_pk)
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                return Response(status=400, data={"error": "Amenity does not exist"})
        else:
            return Response(status=400)


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=404)

    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = RoomDetailSerializer(room, context={"request": request})
            return Response(data=serializer.data)
        except Room.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk):
        room = self.get_object(pk)

        if room.owner.pk != request.user.pk:
            return Response(status=403, data={"error": "Forbidden"})
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(status=404, data={"error": "Room not found"})

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner.pk != request.user.pk:
            return Response(status=403, data={"error": "Forbidden"})
        room.delete()
        return Response(status=204, data={"message": "Room deleted"})


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=404, data={"error": "Room not found"})

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(room.reviews.all(), many=True)
        return Response(data=serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(room=room, user=request.user)
            serializer = ReviewSerializer(review)
            return Response(data=serializer.data)
        else:
            return Response(status=400, data={"error": "Bad Request"})


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=404, data={"error": "Room not found"})

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 2
        start = page_size * (page - 1)
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitySerializer(room.amenity.all()[start:end], many=True)
        return Response(data=serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=404, data={"error": "Room not found"})

    def get(self, request, pk):
        return Response(status=200)

    def post(self, request, pk):
        room = self.get_object(pk)
        if room.owner.pk != request.user.pk:
            return Response(status=403, data={"error": "Forbidden"})
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(data=serializer.data)
        else:
            return Response(status=400, data={"error": "Bad Request"})


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=404, data={"error": "Room not found"})

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()

        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(data=serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors, status=400)
