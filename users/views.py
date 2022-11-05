import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from . import models, serializers


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required")
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = models.User.objects.get(username=username)
            serializer = serializers.TinyUserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError("Password is required")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Username and password are required")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "welcome"}, status=status.HTTP_200_OK)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Invalid username or password"},
            )


class LogOut(APIView):
    def post(self, request):
        permission_classes = [IsAuthenticated]

        logout(request)
        return Response(status=status.HTTP_200_OK, data={"ok": "bye"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Username and password are required")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            payload = {"pk": user.pk}
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Invalid username or password"},
            )
