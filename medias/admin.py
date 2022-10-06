from django.contrib import admin
from .models import Photo, Video

# Register your models here.


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return obj.file.url

    get_thumbnail.short_description = "Thumbnail"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Video Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return obj.file.url

    get_thumbnail.short_description = "Thumbnail"
