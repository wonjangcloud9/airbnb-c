from django.contrib import admin
from .models import Room, Amenity

# Register your models here.


@admin.action(description="Set all prices to 0")
def set_zero(modeladmin, request, queryset):
    queryset.update(price=0)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    actions = (set_zero,)

    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "total_amenities",
        "created_at",
        "rating",
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

    search_fields = (
        "^name",
        "=price",
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
