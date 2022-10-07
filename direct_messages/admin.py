from django.contrib import admin
from .models import ChattingRoom, Message

# Register your models here.


@admin.register(ChattingRoom)
class ChattingRoomAdmin(admin.ModelAdmin):
    """ChattingRoom Admin Definition"""

    list_display = ("__str__", "created_at", "updated_at")

    def __str__(self):
        return "Hi"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Message Admin Definition"""

    list_display = ("message", "user", "room", "created_at", "updated_at")

    def __str__(self):
        return f"{self.user} says: {self.message}"
