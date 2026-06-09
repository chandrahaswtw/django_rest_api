from django.contrib.auth import get_user_model
from core.models import Recipe, Tag
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer, RecipeViewSerializer

from rest_framework.test import APIClient
from rest_framework import status

import tempfile
import os
from PIL import Image

LIST_RECIPE_URL = "recipe:recipe-list"
DETAIL_ALL_RECIPE_URL = "recipe:recipe-detail"


class PublicRecipeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_recipe_page_not_accessible_without_authentication(self):
        res = self.client.get(reverse(LIST_RECIPE_URL))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):

    def create_recipe(self):
        recipe_payload = {
            "user": self.user,
            "title": "test_title1",
            "description": "test_description1",
            "time_minutes": 100,
            "price": 10.00,
            "link": "https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
        }
        return Recipe.objects.create(**recipe_payload)

    def setUp(self):

        user_payload = {
            "email": "test@example.com",
            "password": "Admin@789",
            "name": "Chandrahas Balleda",
        }
        self.user = get_user_model().objects.create_user(**user_payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_recipe_page_if_data_is_loaded_as_expected(self):
        """
        Test id recipes data is loaded correctly
        """

        # Create 2 recipes
        Recipe.objects.bulk_create(
            [
                Recipe(
                    user=self.user,
                    title="test_title1",
                    description="test_description1",
                    time_minutes=100,
                    price=10.00,
                    link="https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
                ),
                Recipe(
                    user=self.user,
                    title="test_title2",
                    description="test_description2",
                    time_minutes=200,
                    price=20.00,
                    link="https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
                ),
            ]
        )

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        res = self.client.get(reverse(LIST_RECIPE_URL))

        # Check if page is loaded successfully
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Check if both outputs are the same
        self.assertEqual(serializer.data, res.data)

    def test_user_only_see_his_recipes(self):
        """
        The user should see his recipes only on UI
        """

        another_user_payload = {
            "email": "test2@example.com",
            "password": "Admin@789",
            "name": "Chandrahas Balleda",
        }
        another_user = get_user_model().objects.create_user(**another_user_payload)

        Recipe.objects.bulk_create(
            [
                Recipe(
                    user=self.user,
                    title="test_title1",
                    description="test_description1",
                    time_minutes=100,
                    price=10.00,
                    link="https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
                ),
                Recipe(
                    user=another_user,
                    title="test_title2",
                    description="test_description2",
                    time_minutes=200,
                    price=20.00,
                    link="https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
                ),
            ]
        )

        recipes = Recipe.objects.filter(user=self.user).order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        res = self.client.get(reverse(LIST_RECIPE_URL))

        # Check if page is loaded successfully
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Check if both outputs are the same
        self.assertEqual(serializer.data, res.data)

    def test_create_recipe(self):

        recipe_payload = {
            "user": self.user,
            "title": "test_title1",
            "description": "test_description1",
            "time_minutes": 100,
            "price": 10.00,
            "link": "https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
            "tags": [{"name": "tag1"}],
        }

        res = self.client.post(reverse(LIST_RECIPE_URL), recipe_payload)

        # Check is record is created successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        record_from_db = Recipe.objects.get(id=res.data["id"])

        # Passed the
        serializer = RecipeSerializer(record_from_db)

        # Can't do this as res.data is a dictionary and record_from_db is an object.
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe(self):

        recipe_payload = {
            "user": self.user,
            "title": "test_title1",
            "description": "test_description1",
            "time_minutes": 100,
            "price": 10.00,
            "link": "https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
        }

        tag = Tag.objects.create(name="tag1", user=self.user)

        record_from_db = Recipe.objects.create(**recipe_payload)
        record_from_db.tags.add(tag)
        serializer = RecipeViewSerializer(record_from_db)

        res = self.client.get(reverse(DETAIL_ALL_RECIPE_URL, args=[record_from_db.id]))

        # Check is record is created successfully
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Can't do this as res.data is a dictionary and record_from_db is an object.
        self.assertEqual(res.data, serializer.data)

    def test_update_recipe(self):

        recipe_payload = {
            "user": self.user,
            "title": "test_title1",
            "description": "test_description1",
            "time_minutes": 100,
            "price": 10.00,
            "link": "https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
        }

        tag = Tag.objects.create(name="tag1", user=self.user)
        record_from_db = Recipe.objects.create(**recipe_payload)
        record_from_db.tags.add(tag)

        recipe_payload_patch = {
            "id": record_from_db.id,
            "title": "test_title2",
            "tags": [{"name": "tag2"}],
        }

        res = self.client.patch(
            reverse(DETAIL_ALL_RECIPE_URL, args=[record_from_db.id]),
            recipe_payload_patch,
        )

        # Fetch value from DB again
        record_from_db.refresh_from_db()

        # Check is record is created successfully
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            RecipeSerializer(record_from_db).data,
        )


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@example.com",
            "password123",
        )
        self.client.force_authenticate(self.user)

        recipe_payload = {
            "user": self.user,
            "title": "test_title1",
            "description": "test_description1",
            "time_minutes": 100,
            "price": 10.00,
            "link": "https://en.wikipedia.org/wiki/Breaking_the_Habit_(song)",
        }
        self.recipe = Recipe.objects.create(**recipe_payload)

    # We need to do this to delete the uploaded image
    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a recipe."""
        url = reverse("recipe:recipe-upload-image", args=[self.recipe.id])
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"image": image_file}
            res = self.client.post(url, payload, format="multipart")

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = reverse("recipe:recipe-upload-image", args=[self.recipe.id])
        payload = {"image": "notanimage"}
        res = self.client.post(url, payload, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
