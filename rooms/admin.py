from django.contrib import admin
from .models import Room, Amenity

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "address",
        "pet_allowed",
        "kind",
        "owner",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_allowed",
        "kind",
        "owner",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    """Amenity Admin Definition"""

    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
