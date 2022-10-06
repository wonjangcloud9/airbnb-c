from django.db import models
from common.models import CommonModel

# Create your models here.


class ChattingRoom(CommonModel):

    """Room Model Definition"""

    participants = models.ManyToManyField(
        "users.User",
    )


class Message(CommonModel):

    """Message Model Definition"""

    message = models.TextField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
    )
