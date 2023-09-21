from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, status
from rest_framework import response
from django.contrib.auth.hashers import check_password

from django.contrib.auth import authenticate
from .utils import response, abort, BaseResponse
from .models import OrganizationInvites, Users
from rest_framework.exceptions import AuthenticationFailed
from .utils import response, abort, BaseResponse, generate_token, EmailManager
from .serializers import (GetOrganizationSerializer, LoginSerializer,
                          InviteSerializer, RegisterSerializer, UserListSerializer)
from .tokens import create_jwt_pair_for_user


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
    # queryset = OrganizationInvites
    permission_classes = [AllowAny]


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
                        context={'organization':invite, 'token':token}
                    )
        data = {
            'reciepient_email': invite.email,
            'token': invite.token,
            'TTL': invite.TTL
        }
        res = {
            "message": "Invite sent!",
            "code":201,
            "data":data
        }
        return Response(data=res, status=status.HTTP_201_CREATED)
    



class RegisterUserView(generics.CreateAPIView):
    """View for handling user registration.
    This view handles user registration and returns a response with the serialized data of the newly created user.
    """

    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        exception = None
        try:
            email = request.data.get('email')
            org_invite = OrganizationInvites.objects.filter(email=email).first()
            org = org_invite.org_id if org_invite else None

            serializer = RegisterSerializer(data=request.data, context={'org': org})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            response_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
            base_response = BaseResponse(data=response_data,exception=exception, message="User Created Successfully")
            return Response(base_response.to_dict(), status=status.HTTP_201_CREATED)

        except Exception as e:
            return abort(404, "Email not invited")


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

            if not email or not password:
                raise AuthenticationFailed('Both email and password is required')

            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    tokens=create_jwt_pair_for_user(user)
                    return Response({
                        "message": "User authenticated successfully",
                        "status": 200,
                        "id": user.id,
                        "tokens": tokens
                    })
                else:
                    raise AuthenticationFailed("User Is not active")
            raise AuthenticationFailed("Invalid Email o password")

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

class UsersListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserListSerializer

    def get_queryset(self):
        org_id = self.kwargs.get('org_id', None)
        if org_id:
            queryset = Users.objects.filter(org_id=org_id)
        else:
            queryset = Users.objects.all()
        return queryset
