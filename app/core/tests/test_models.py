from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_user_model(self):
        email = "test@example.com"
        password = "User@789"

        # Get get_user_model as name suggests gave the user model and we can run queries on it.
        user = get_user_model().objects.create_user(email=email, password=password)

        # We created the user and checing the details
        self.assertEqual(user.email, email)

        # Since password is hashed, user.check_password verifies the password.
        self.assertTrue(user.check_password(password))

    def test_normalize_users(self):
        emails = [
            ("test@example.com", "test@example.com"),
            ("test1@example.COM", "test1@example.com"),
            ("test2@exampLE.com", "test2@example.com"),
            ("test3@Example.com", "test3@example.com"),
        ]
        password = "Abc@123"

        for email, expected_email in emails:
            user = get_user_model().objects.create_user(email=email, password=password)
            self.assertEqual(user.email, expected_email)

    def test_not_allow_blank_emails(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="User@789")

    def test_superuser(self):
        email = "test@example.com"
        password = "Admin@789"

        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
