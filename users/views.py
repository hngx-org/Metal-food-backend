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
from rest_framework import response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password

from django.contrib.auth import authenticate
from .utils import response, abort, BaseResponse
from .models import Users, Organization, OrganizationInvites
from rest_framework.exceptions import AuthenticationFailed
from .utils import response, abort, BaseResponse, generate_token, EmailManager
from .serializers import (GetOrganizationSerializer, LoginSerializer,
                          InviteSerializer, RegisterSerializer)


# User = get_user_model()

class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = GetOrganizationSerializer
    permission_classes = [AllowAny]

    def create(self, request):
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


class CreateInviteView(generics.CreateAPIView):
    serializer_class = InviteSerializer
    queryset = OrganizationInvites
    # permission_classes = [is]


    def create(self, request):
        token = generate_token()
        email = request.data.get('email')
        serializer = self.get_serializer(data=request.data, context={'token':token})
        serializer.is_valid(raise_exception=True)
        invite = serializer.save()
        EmailManager.send_mail(
                        subject=f"Your invite token is {invite.token}.",
                        recipients=[email],
                        template_name="user_invite.html",
                    )
        res = {
            "message": "Invite sent!",
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


class LoginView(APIView):
    """
     handles both organizatio and user
     login requests
    """
    
    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        
        if login_serializer.is_valid(raise_exception=True):
            email = request.data.get('email')
            password = request.data.get('password')

            user = authenticate(email=email, password=password)
            if not email or not password:
                raise AuthenticationFailed('Both email and password is required')
            
            if user is not None:
                if user.is_active:
                   refresh = RefreshToken.for_user(user)
                   access_token = str(refresh.access_token) 
   
                   return Response({
                        "message": "User authenticated successfully",
                        "status": 200,
                        "user": user.id,
                        "token": access_token
                    })
        # if login_serializers.is_valid(raise_exception=True): 
        #     email = request.data.get('email')
        #     password = request.data.get('password')

        #     user = Users.objects.filter(email=email).first()
        #     organization = Organization.objects.filter(email=email).first()

        #     # checks if user organzation email exists
        #     if organization is None and check_password(password=password):
        #         raise AuthenticationFailed("Email Not found") 
            
        #     else:
        #         refresh = RefreshToken.for_user(user)
        #         access_token = str(refresh.access_token)
        #         return response({"message": "User authenticated successfully",
        #                         "status": 200,
        #                         "token": access_token,
        #                         "email": Users.objects.filter(email=email).first(),
        #                         "id": Users.objects.get(email=email).id,
        #                         "is_admin": User.is_admin
        #                         },
        #                         status=status.HTTP_200_OK)

        #     # checks for organization valid password or user
        #     # valid password
        #     if (not user.check_password(password) or
        #         not organization.check_password(password)
        #         ):
        #         raise AuthenticationFailed("Incorrect password")
            
        #     else:
        #         refresh = RefreshToken.for_user(user)
        #         access_token = str(refresh.access_token)
             
        #         return response({"message": "User authenticated successfully",
        #                         "status": 200,
        #                         "token": access_token,
        #                         }
        #                         status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if refresh_token:
            # Blacklist the refresh token
            try:
                RefreshToken(token=refresh_token).blacklist()
                return Response({"message": "Logout successful"},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return response({"error": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)