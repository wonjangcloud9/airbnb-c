from django.db import models
from common.models import CommonModel

# Create your models here.


class WishList(CommonModel):

    """WishList Model Definition"""

    name = models.CharField(
        max_length=150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name="wishlists",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name="wishlists",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlists",
    )
