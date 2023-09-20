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



# User = get_user_model()

class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = GetOrganizationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        print(org.__dict__)
        res = {
            "message": "Organization created successfully!",
            "code":201,
            "data":serializer.data
        }
        return Response(data=res, status=status.HTTP_201_CREATED)



class RegisterView(generics.CreateAPIView):
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
                'full_name': user.full_name,
                'email': user.email,
            }
            base_response = BaseResponse(data=response_data, exception=exception, message="User Created Successful")
            return Response(base_response.to_dict())
        except Exception as e:
            return abort(400, "User registration failed" + str(e))

            
        return Response(response_data, status=status.HTTP_201_CREATED)