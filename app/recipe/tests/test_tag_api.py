from django.contrib.auth import get_user_model
from core.models import Tag
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import TagSerializer

from rest_framework.test import APIClient
from rest_framework import status

LIST_TAG_URL = "recipe:tag-list"
DETAIL_TAG_URL = "recipe:tag-detail"


class PublicTagAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_recipe_page_not_accessible_without_authentication(self):
        res = self.client.get(reverse(LIST_TAG_URL))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagAPITests(TestCase):

    def setUp(self):

        user_payload = {
            "email": "test@example.com",
            "password": "Admin@789",
            "name": "Chandrahas Balleda",
        }
        self.user = get_user_model().objects.create_user(**user_payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_tag_list(self):

        # Creating few tags
        Tag.objects.create(name="tag1", user=self.user)
        Tag.objects.create(name="tag2", user=self.user)

        res = self.client.get(reverse(LIST_TAG_URL))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Fetch records form DB and get return data from serilalizer
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        # Check if they are the same
        self.assertEqual(serializer.data, res.data)

    def test_tag_create(self):

        tag_payload = {"user": self.user, "name": "tag1"}

        res = self.client.post(reverse(LIST_TAG_URL), tag_payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Fetch records form DB
        doesTagExists = Tag.objects.filter(**tag_payload).exists()

        self.assertTrue(doesTagExists)

    def test_tag_delete(self):

        tag = Tag.objects.create(name="tag1", user=self.user)

        res = self.client.delete(reverse(DETAIL_TAG_URL, args=[tag.id]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
