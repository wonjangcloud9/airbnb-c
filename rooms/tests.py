from rest_framework.test import APITestCase
from . import models


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESCRIPTION = "Amenity Test Description"
    URL = "/api/v1/rooms/amenities"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESCRIPTION)

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 200, "Status code should be 200")
        self.assertIsInstance(data, list, "Data should be a list")
        self.assertEqual(len(data), 1, "Data should have 1 item")
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESCRIPTION)

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc."

        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_description,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["name"],
            new_amenity_name,
        )
        self.assertEqual(
            data["description"],
            new_amenity_description,
        )
