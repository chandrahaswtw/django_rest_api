from django.urls import path
from .views import CreateUserApiView, GetTokenApiView, ManageUserAPIView

app_name = "user"

urlpatterns = [
    path("create", CreateUserApiView.as_view(), name="create"),
    path("token", GetTokenApiView.as_view(), name="token"),
    path("me", ManageUserAPIView.as_view(), name="me"),
]
