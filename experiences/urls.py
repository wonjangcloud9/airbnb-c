from django.urls import path
from .views import Perks, PerkDetail

app_name = "experiences"

urlpatterns = [
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>/", PerkDetail.as_view()),
]
