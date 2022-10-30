from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WishList
from rooms.models import Room
from .serializers import WishListSerializer


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = WishList.objects.filter(user=request.user)
        serializer = WishListSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishListSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishListSerializer(wishlist)
            return Response(serializer.data)
        return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            return Response(status=404)

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishListSerializer(
            wishlist,
        )
        return Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishListSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishListSerializer(wishlist)
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response({"message": "Wishlist deleted"}, status=204)


class WishListToggle(APIView):
    def get_list(self, pk, user):
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            return Response(status=404)

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=200)
