from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import LoginSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status



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