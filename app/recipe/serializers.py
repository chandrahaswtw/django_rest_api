from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from user.serializers import UserSerializer
from rest_framework import serializers
from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "time_minutes",
            "price",
            "link",
            "description",
            "tags",
        ]

        # This field can be returned in API responses, but clients are not allowed to provide or modify it. Opposite of write_only
        #  We can use the same as
        #  extra_kwargs = {
        #     "id": {"read_only": True}
        # }
        read_only_fields = ["id"]

    def create(self, validated_data):

        # Fetch user
        user = self.context["request"].user

        # Pop out the tags
        tags = validated_data.pop("tags", None)

        # Create recipe
        recipe = Recipe.objects.create(**validated_data)

        # Loop through the tags and add it in recipe.
        if tags is not None:
            for tag in tags:
                created_tag, created = Tag.objects.get_or_create(user=user, **tag)
                recipe.tags.add(created_tag)

        return recipe

    def update(self, instance, validated_data):
        # Instance is the model actual instance we can perform tasks.

        # Fetch user
        user = self.context["request"].user

        # Pop out the tags
        tags = validated_data.pop("tags", None)

        # Clear out the tags in current instance
        instance.tags.clear()

        # Loop through the tags and add it in recipe.
        if tags is not None:
            for tag in tags:
                created_tag, created = Tag.objects.get_or_create(user=user, **tag)
                instance.tags.add(created_tag)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return super().update(instance, validated_data)


class RecipeViewSerializer(RecipeSerializer):

    user = UserSerializer(required=False)

    class Meta(RecipeSerializer.Meta):
        model: Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags", "user"]
