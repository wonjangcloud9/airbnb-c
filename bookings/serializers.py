from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Check in date should be after today")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Check in date should be after today")
        return value

    def create(self, validated_data):
        guests = self.context.get("guests")
        room = validated_data.get("room")
        check_in = validated_data.get("check_in")
        check_out = validated_data.get("check_out")
        booking = Booking.objects.create(
            guests=guests,
            room=room,
            check_in=check_in,
            check_out=check_out,
        )
        return booking


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
