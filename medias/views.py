from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Photo
from rest_framework.response import Response


class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise Response(status=404)

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            return Response(status=403)
        photo.delete()
        return Response(status=200)
