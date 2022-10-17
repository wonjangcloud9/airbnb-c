from django.contrib import admin
from .models import Photo, Video

# Register your models here.


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = ("__str__",)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Video Admin Definition"""

    list_display = ()
