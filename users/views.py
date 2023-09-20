import re

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
from rest_framework import permissions
from .serializers import UserSerializer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password

from .serializers import *
from .utils import response, abort, BaseResponse



User = get_user_model()


# class RegisterView(generics.CreateAPIView):
#     """View for handling user registration.
#     This view handles user registration and  returns a response with the serialized data of the newly created user.
#     """

#     authentication_classes = ()
#     permission_classes = ()
#     serializer_class = RegisterSerializer
#     def create(self, request, *args, **kwargs):
#         exception = None
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             user = serializer.save()

#             response_data = {
#                 'full_name': user.full_name,
#                 'email': user.email,
#             }
#             base_response = BaseResponse(data=response_data, exception=exception, message="User Created Successful")
#             return Response(base_response.to_dict())
#         except Exception as e:
#             return abort(400, "User registration failed" + str(e))

            
#         return Response(response_data, status=status.HTTP_201_CREATED)

class UsersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        org_id = self.kwargs.get('org_id')
        queryset = Users.objects.filter(org_id=org_id)
        return queryset
    

class UsersView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request):
        """ 
        Create a new user
        """
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        pattern = r'\d'
        if re.search(pattern, first_name) or re.search(pattern, last_name):
            return Response(data={
                'message' : 'First name and last name cannot contain numbers',
                'code' : 400,
                'data' : {}
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "message": "User created successfully!",
                "code": 201,
                "data":serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(data={
            "message":serializer.errors,
            "code":400,
            "data":{}
        }, status=status.HTTP_400_BAD_REQUEST)
