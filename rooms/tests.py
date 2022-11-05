from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESCRIPTION = "Amenity Test Description"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESCRIPTION)

    def test_get_amenities(self):
        response = self.client.get("/api/v1/rooms/amenities")
        data = response.json()
        self.assertEqual(response.status_code, 200, "Status code should be 200")
        self.assertIsInstance(data, list, "Data should be a list")
        self.assertEqual(len(data), 1, "Data should have 1 item")
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESCRIPTION)
