from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, status

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password

from .serializers import *
from .utils import response, abort, BaseResponse



User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    """View for handling user registration.
    This view handles user registration and  returns a response with the serialized data of the newly created user.
    """

    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        exception = None
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            response_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
            base_response = BaseResponse(data=response_data, exception=exception, message="User Created Successful")
            return Response(base_response.to_dict())
        except Exception as e:
            return abort(400, "User registration failed" + str(e))


class RegisterOrganisationView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = 