from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


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

    def test_user_return_token_after_successful_authentication(self):
        """
        Test if token is present after succsful authentication
        """
        payload = {
            "email": "test@example.com",
            "password": "User@789",
            "name": "Tester",
        }

        # Creating record directly using get_user_model
        get_user_model().objects.create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_not_return_token_after_failed_authentication(self):
        """
        Test if token not present after failed authentication
        """
        payload = {
            "email": "test@example.com",
            "password": "User@789",
            "name": "Tester",
        }

        # Creating record directly using get_user_model
        get_user_model().objects.create_user(**payload)

        payload_wrong = {
            "email": "test@example.com",
            "password": "Userss",
            "name": "Tester",
        }

        res = self.client.post(TOKEN_URL, payload_wrong)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_view_without_authentication(self):
        """
        Cannot view the self data when not authorized
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiUserTests(TestCase):
    """
    Public API tests
    """

    payload = {
        "email": "test@example.com",
        "password": "User@789",
        "name": "Tester",
    }

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=self.payload["email"],
            password=self.payload["password"],
            name=self.payload["name"],
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_can_view_with_authentication(self):
        """
        Can view the self data when authorized
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "email": "test@example.com",
                "name": "Tester",
            },
        )

    def test_user_can_update_with_authentication(self):
        """
        Can update the self data when authorized
        """

        new_payload = {
            "password": "User@789New",
            "name": "Tester_ha",
        }
        res = self.client.patch(ME_URL, new_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Refreshes its data from DB
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, new_payload["name"])
        self.assertTrue(self.user.check_password(new_payload["password"]))
