from django.contrib import admin
from .models import Experience, Perk

# Register your models here.


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "detail",
        "explanation",
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "country",
        "city",
        "name",
        "host",
        "price",
        "address",
        "start",
        "end",
        "description",
    )

    list_filter = (
        "country",
        "city",
        "name",
        "host",
        "price",
        "address",
        "start",
        "end",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
