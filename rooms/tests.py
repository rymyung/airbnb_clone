from rest_framework.test import APITestCase

from users.models import User

from .models import Amenity


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESCRIPTION = "Amenity Test Desc"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self) -> None:
        Amenity.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
        )

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status cod isn't 200.")
        self.assertIsInstance(data, list, "It should be list.")
        self.assertEqual(len(data), 1, "It should be 1.")
        self.assertEqual(data[0]["name"], self.NAME)
        self.assertEqual(data[0]["description"], self.DESCRIPTION)

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_desc = "New Amenity Desc"
        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_desc,
            }
        )
        data = response.json()

        self.assertEqual(response.status_code, 200, "Not 200 status code.")
        self.assertEqual(data["name"], new_amenity_name)
        self.assertEqual(data["description"], new_amenity_desc)

        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenity(APITestCase):

    NAME = "Amenity Test"
    DESCRIPTION = "Amenity Test Desc"
    URL = "/api/v1/rooms/amenities"

    def setUp(self) -> None:
        Amenity.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
        )

    def test_amenity_not_found(self):

        response = self.client.get(f"{self.URL}/2")
        self.assertEqual(response.status_code, 404)


    def test_get_amenity(self):

        response = self.client.get(f"{self.URL}/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESCRIPTION)

    def test_update_amenity(self):
        pass

    def test_delete_amenity(self):

        response = self.client.delete(f"{self.URL}/1")
        self.assertEqual(response.status_code, 204)


class TestRoom(APITestCase):

    def setUp(self) -> None:

        user = User.objects.create(username="test")
        user.set_password("test")
        user.save()

        self.user = user

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user)

        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 400)
