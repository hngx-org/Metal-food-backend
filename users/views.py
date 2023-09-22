from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import permissions
from .serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Users, OrganizationLunchWallet, OrganizationInvites

from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import *

from .tokens import create_jwt_pair_for_user
from .utils import EmailManager, generate_token, BaseResponse

class AddBankAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = BankAccountSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            user_data = {
                "email": user.email,  
                "bank_number": user.bank_number,  
                "bank_code": user.bank_code,
                "bank_name": user.bank_name,
            }
            return Response({ 
                "data": user_data,
                "message": "Bank account information updated successfully",
                "code": 200, 
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = GetOrganizationSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        data = {
            "id": org.id,
            "name": org.name,
            "email": org.email,
            "lunch_price": org.lunch_price,
            "currency": org.currency,
            "created_at": org.created_at,
            "password": org.password,
        }
        res = {
            "message": "Organization created successfully!",
            "code": 201,
            "data": data,
        }
        return Response(data=res, status=status.HTTP_201_CREATED)


class CreateInviteView(generics.CreateAPIView):
    serializer_class = InviteSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        token = generate_token()
        serializer = self.get_serializer(data=request.data, context={"token": token})
        serializer.is_valid(raise_exception=True)
        invite = serializer.save()

        EmailManager.send_mail(
            subject=f"Free Lunch Invite.",
            recipients=[invite.email],
            template_name="user_invite.html",
            context={"organization": invite.org_id, "token": invite.token},
        )

        data = {
            "reciepient_email": invite.email,
            "token": invite.token,
            "TTL": invite.TTL,
        }
        res = {"message": "Invite sent!", "code": 200, "data": data}
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
            email = request.data.get("email")
            org_invite = OrganizationInvites.objects.filter(email=email).first()
            org = org_invite.org_id if org_invite else None

            serializer = RegisterSerializer(data=request.data, context={"org": org})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            response_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
            base_response = BaseResponse(
                data=response_data,
                exception=exception,
                message="User Created Successfully",
            )
            return Response(base_response.to_dict(), status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    handles both organization and user
    login requests
    """

    permission_classes = [AllowAny]

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)

        # checks if serializer data is valid

        if login_serializer.is_valid(raise_exception=True):
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or password:
                raise AuthenticationFailed("Both emil and password is required")

            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    tokens = create_jwt_pair_for_user(user)
                    return Response(
                        {
                            "message": "User authenticated successfully",
                            "status": 200,
                            "id": user.id,
                            "token": tokens,
                        }
                    )


class LogoutView(APIView):
    """
    Handle user logout request
    """

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if refresh_token:
            try:
                RefreshToken(token=refresh_token).blacklist()
                return Response(
                    {"message": "Logout successfully"}, status=status.HTTP_20O_OK
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )



class UpdateOrganizationLunchWallet(APIView):

    """
    Title: Update Organization launch wallet balance
    Description: Description: Allows an admin user to update wallet balance.

    Endpoint: /api/<id>/organization/wallet/update
    Method:PATCH
    """

    queryset = OrganizationLunchWallet.objects.all()

    def patch(self, request, org_id):
        wallet = OrganizationLunchWallet.objects.get(org_id=org_id)
        serializer = LunchWalletSerializer(wallet, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "success", "status": 200, "data": serializer.data}
            )
        return Response({"message": "error", "error": serializer.errors})


class ListUsersView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = AllUserSerializer
    permission_classes = [IsAuthenticated]


class SearchUserView(generics.RetrieveAPIView):
    serializer_class = AllUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        nameoremail = self.kwargs.get(
            "nameoremail"
        )  # Get the nameoremail parameter from the URL
        # Perform a case-insensitive search on first_name, last_name, and email
        queryset = Users.objects.filter(
            Q(first_name__icontains=nameoremail)
            | Q(last_name__icontains=nameoremail)
            | Q(email__icontains=nameoremail)
        )
        return queryset

    def retrieve(self, request, nameoremail):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset)
        serializer = AllUserSerializer(user)
        return Response(
            {
                "message": "User found",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data,
            }
        )


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        response = {
            "message": "User data fetched successfully",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
