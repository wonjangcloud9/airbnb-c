from django.db import models


class House(models.Model):

    """House Model Definition"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField(
        verbose_name="Price", help_text="Positive Numbers Only"
    )
    description = models.TextField()
    address = models.CharField(max_length=140)
    pet_allowed = models.BooleanField(
        verbose_name="Pet Allowed", default=True, help_text="Can you bring your pet?"
    )
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="houses"
    )

    def __str__(self):
        return self.name
