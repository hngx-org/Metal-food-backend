from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import generics
from .serializers import *
from .utils import *




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
     handles both organization and user
     login requests
    """
    def post(self, request):
        permission_classes = [IsAuthenticated]
        login_serializer = LoginSerializer(data=request.data)

        # checks if serializer data is valid
        
        if login_serializer.is_valid(raise_exception=True):
            email = request.data.get('email')
            password = request.data.get('password')
            
            if not email or password:
                raise AuthenticationFailed("Both emil and password is required")

            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    tokens = create_jwt_pair_for_user(user)
                    return Response({
                        "message": "User authenticated successfully",
                        "status": 200,
                        "id": user.id,
                        "token": tokens
                    })


class LogoutView(APIView):
    """
        Handle user logout request
    """
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        
        if refresh_token:
            try:
                RefreshToken(token=refresh_token).blacklist()
                return Response({"message": "Logout successfully"},
                                status=status.HTTP_20O_OK
                                )
            except Exception as e:
                return Response({"error": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        
        else:
            Response({"error": "Refresh token is required"},
                            status=status.HTTP_400_BAD_REQUEST
                            )