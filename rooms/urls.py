from django.urls import path
from . import views

urlpatterns = [
    path("amenities/", views.Amenities.as_view(), name="amenity-list"),
    path("amenities/<int:pk>", views.AmenityDetail.as_view(), name="amenity-detail"),
]
