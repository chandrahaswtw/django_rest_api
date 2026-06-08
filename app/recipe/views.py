from rest_framework import viewsets, authentication, permissions
from .serializers import RecipeSerializer, RecipeViewSerializer, TagSerializer
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

        return RecipeSerializer


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
