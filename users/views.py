from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import permissions
from .serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Users, OrganizationLunchWallet, OrganizationInvites
from rest_framework_simplejwt.authentication import JWTAuthentication
<<<<<<< HEAD
from django.contrib.auth import authenticate, get_user_model, login
=======
from django.contrib.auth import get_user_model
>>>>>>> 5c724e48eb989633ffb9ee6a0d47d6c630d28e15
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import *

from .tokens import create_jwt_pair_for_user
from .utils import EmailManager, generate_token, BaseResponse
from .backends import CustomUserBackend


User = get_user_model()

# Do not use `User` from `get_user_model()` above with `authenticate` below
# Where User or Oganization model is needed for authetication, import directly form `users.models`
authenticate = CustomUserBackend.authenticate


class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = GetOrganizationSerializer
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
    permission_classes = [AllowAny]
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
            user.is_active = True

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


# class RegisterOrganisationView(generics.CreateAPIView):
    



class LoginView(APIView):
    """
    Handles both organization and user login requests and returns refresh and access tokens.
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if the email exists in the Organization model
        organization = Organization.objects.filter(email=email).first()
        
        if organization:
            user = authenticate(request, email=email, password=password, is_user=False)
        else:
            # Check if the email exists in the Users model
            user = authenticate(request, email=email, password=password, is_user=True)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):
    """
    View to logout a user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
           
            token = RefreshToken(refresh_token)
            token.blacklist()
            base_response = BaseResponse(None, None, 'Successfully logged out.')
            return Response(base_response.to_dict(), status=status.HTTP_200_OK)
        except Exception as e:
            print(type(str(e)))
            return abort(400, str(e))



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
    # authentication_classes = [JWTAuthentication]
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
        current_user = request.user
        serializer = self.get_serializer(current_user)
        response = {
            "message": "User data fetched successfully",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)



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
