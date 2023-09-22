from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import generics
from .serializers import *
from .utils import *

from .serializers import GetOrganizationSetializer, InviteSerializer
from .tokens import create_jwt_pair_for_user
from .utils import EmailManager, generate_token

# Create your views here.

class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = GetOrganizationSetializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        data = {
            'id':org.id,
            'name':org.name,
            'email':org.email,
            'lunch_price':org.lunch_price,
            'currency':org.currency,
            'created_at':org.created_at,
            'password':org.password
        }
        res = {
            "message": "Organization created successfully!",
            "code":201,
            "data":data
        }
        return Response(data=res, status=status.HTTP_201_CREATED)


class CreateInviteView(generics.CreateAPIView):
    serializer_class = InviteSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        token = generate_token()
        serializer = self.get_serializer(data=request.data, context={'token':token})
        serializer.is_valid(raise_exception=True)
        invite = serializer.save()

        EmailManager.send_mail(
            subject=f"Free Lunch Invite.",
            recipients=[invite.email],
            template_name="user_invite.html",
            context={"organization":invite.org_id, 'token':invite.token}
        )

        data = {
            'reciepient_email': invite.email,
            'token': invite.token,
            'TTL': invite.TTL
        }
        res = {
            "message": "Invite sent!",
            "code":200,
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

