from django.db import models
from common.models import CommonModel


class Room(CommonModel):

    """Room Model Definition"""

    class RoomChoices(models.TextChoices):
        ENTIRE = "entire", "Entire Place"
        PRIVATE = "private", "Private Room"
        SHARED = "shared", "Shared Room"

    name = models.CharField(max_length=180, default="")
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_allowed = models.BooleanField(default=True)
    kind = models.CharField(
        max_length=10,
        choices=RoomChoices.choices,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    amenity = models.ManyToManyField(
        "rooms.Amenity",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    def total_amenities(self):
        return self.amenity.count()


class Amenity(CommonModel):

    """Amenity Model Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
