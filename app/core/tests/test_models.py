from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Recipe, Tag, recipe_image_file_Path
from unittest.mock import patch


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


class RecipeModelTests(TestCase):

    user_payload = {
        "email": "test@example.com",
        "password": "Admin@789",
        "name": "Chandrahas Balleda",
    }

    def create_user(self):
        """
        Create new user function
        """
        return get_user_model().objects.create_user(**self.user_payload)

    def test_recipe_record_creation(self):
        user = self.create_user()

        recipe_payload = {
            "user": user,
            "title": "test_title",
            "description": "test_description",
            "time_minutes": 100,
            "price": 23.33,
            "link": "https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
        }

        recipe = Recipe.objects.create(**recipe_payload)

        self.assertEqual(recipe.title, recipe_payload["title"])


class TagModelTests(TestCase):
    def test_tag_model(self):
        user_payload = {
            "email": "test@example.com",
            "password": "Admin@789",
            "name": "Chandrahas Balleda",
        }
        user = get_user_model().objects.create_user(**user_payload)
        tag = Tag.objects.create(name="testTag", user=user)
        self.assertEqual(tag.name, "testTag")


class RecipeModelImageTests(TestCase):

    @patch("core.models.uuid.uuid4")
    def test_recipe_image_file_Path(self, mock_uuid):

        #  Mocked uuid.uuid4() will now return "test_uuid"
        test_uuid = "test_uuid"
        mock_uuid.return_value = test_uuid

        filename = recipe_image_file_Path(None, "something.png")
        self.assertEqual(filename, f"uploads/{test_uuid}.png")
