from rest_framework import viewsets, authentication, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    RecipeSerializer,
    RecipeViewSerializer,
    TagSerializer,
    RecipeImageSerializer,
)
from core.models import Recipe, Tag


class RecipeView(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Recipe.objects.all()

    def get_queryset(self):
        base_query = super().get_queryset()
        return base_query.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RecipeViewSerializer
        if self.action == "upload_image":
            return RecipeImageSerializer

        return RecipeSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Tag.objects.all()

    def get_queryset(self):
        base_query = super().get_queryset()
        return base_query.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
