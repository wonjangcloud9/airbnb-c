from django.db import models


class Room(models.Model):

    """Room Model Definition"""

    class RoomChoices(models.TextChoices):
        ENTIRE = "entire", "Entire Place"
        PRIVATE = "private", "Private Room"
        SHARED = "shared", "Shared Room"

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


class Amenity(models.Model):

    """Amenity Model Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, default="")
