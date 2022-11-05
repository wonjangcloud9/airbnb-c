from rest_framework.test import APITestCase


class TestAmenities(APITestCase):
    def test_get_amenities(self):
        response = self.client.get("/api/v1/rooms/amenities")
        self.assertEqual(response.status_code, 200)
