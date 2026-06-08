"""
URL mappings for the recipe app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe.views import RecipeView, TagView

router = DefaultRouter()
router.register("recipes", RecipeView)
router.register("tags", TagView)

app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]
