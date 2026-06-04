from rest_framework import generics, permissions, authentication
from .serializers import UserSerializer, TokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class CreateUserApiView(generics.CreateAPIView):
    serializer_class = UserSerializer


class GetTokenApiView(ObtainAuthToken):
    serializer_class = TokenSerializer


# We are using RetrieveUpdateAPIView --> helps with both retrieving and updating the data.
#
# The way we authorize on Swagger is:
#   - Click on Authorize on UI
#   - Under token auth, enter Token <Token> example: Token d86f011484902c0b9e33b7d2973b6412650da9e3


class ManageUserAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    # This API is allowed on token authentication. We can have multiple authntication methods.
    authentication_classes = [authentication.TokenAuthentication]

    # Only authenticated users are allowed.
    permission_classes = [permissions.IsAuthenticated]

    # This is used for get requests.
    def get_object(self):
        # Once user is authentcated, it's available on the request.
        return self.request.user
