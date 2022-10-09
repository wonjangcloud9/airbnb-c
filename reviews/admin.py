from django.contrib import admin
from .models import Review

# Register your models here.


class WordFilter(admin.SimpleListFilter):
    title = "word"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return (
            ("15", "15"),
            ("32", "32"),
            ("123", "123"),
        )

    def queryset(self, request, queryset):
        word = self.value()
        if word == "15":
            return queryset.filter(payload__contains="15")
        elif word == "32":
            return queryset.filter(payload__contains="32")
        elif word == "123":
            return queryset.filter(payload__contains="123")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_allowed",
    )
