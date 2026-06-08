from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers
from core.models import Recipe


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"min_length": 5, "write_only": True}}

    # We created explicit function create that overrides the default create function.
    # We did this as because directly password gets saved without encryption. Doing this encrypts it.
    # create_user --> Does the encryption. Just .create don't do it.
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    # We are overriding the update function. Automatically called during updates.
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class TokenSerializer(serializers.Serializer):

    email = serializers.EmailField()

    # style={"input_password": "password"} --> Only for Swagger to make password invisible.
    # trim_whitespace=True --> By default, trim_whitespace is False, we are overriding it.
    password = serializers.CharField(
        style={"input_password": "password"}, trim_whitespace=True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            raise serializers.ValidationError(
                _("Authentication failed"), code="authorization"
            )

        attrs["user"] = user
        return attrs
