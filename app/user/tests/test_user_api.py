from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")


class PublicApiUserTests(TestCase):
    """
    Public API tests
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """
        Tests user creation
        """

        payload = {
            "email": "test@example.com",
            "password": "User@789",
            "name": "Tester",
        }

        # Check if user creation is successful

        # res.status_code has the status code.
        # res.data has the data from the API call.
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Fetch the user and validate the password.
        fetched_user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(fetched_user.check_password(payload["password"]))

        # Check if password should not be present in response
        self.assertNotIn("password", res.data)

    def test_create_user_with_same_email(self):
        """
        Checks if error is thrown if user with same email is created.
        """

        payload = {
            "email": "test@example.com",
            "password": "User@789",
            "name": "Tester",
        }

        # Creating record directly using get_user_model
        get_user_model().objects.create_user(**payload)

        # Since we are trying to insert same user again, should throw the error 400 error.
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_proper_password_requirements(self):
        """
        Checks if error is thrown if short password is entered. It should've min length 5
        """

        payload_improper = {
            "email": "test@example.com",
            "password": "Us",
            "name": "Tester",
        }

        # Since we are trying to insert same user again, should throw the error 400 error.
        res = self.client.post(CREATE_USER_URL, payload_improper)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Confirm user is not created with that bad data
        isUserCreated = (
            get_user_model().objects.filter(email=payload_improper["email"]).exists()
        )
        self.assertFalse(isUserCreated)
