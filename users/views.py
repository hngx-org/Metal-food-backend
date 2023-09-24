from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import permissions
from .serializers import *
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from .models import Users, OrganizationLunchWallet, OrganizationInvites
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import *
from .serializers import LunchWalletSerializer
from .models import OrganizationLunchWallet

from .tokens import create_jwt_pair_for_user
from .utils import EmailManager, generate_token, BaseResponse

from django.core.mail import send_mail

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
    permission_classes = [IsAuthenticated,]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        org.is_active = True
        data = {
            'id':org.id,
            'name':org.name,
            'lunch_price':org.lunch_price,
            'currency':org.currency,
            'created_at':org.created_at,
        }
        res = {
            "message": "Organization created successfully!",
            "code": 201,
            "data": data,
        }
        return Response(data=res, status=status.HTTP_201_CREATED)


class CreateInviteView(generics.CreateAPIView):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        token = generate_token()
        org_id = request.user.organization_id
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


class RegisterSTAFFView(generics.CreateAPIView):
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
            return Response({"Error": "Email not invited to join this organisation"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterUSERView(generics.CreateAPIView):
    """View for handling user registration.
    This view handles user registration and returns a response with the serialized data of the newly created user.
    """

    authentication_classes = ()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        exception = None
        try:

            serializer = RegisterUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print(serializer.errors)
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
            return Response({"Error: ww": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class RegisterOrganisationView(generics.CreateAPIView):
    

from rest_framework_simplejwt.views import TokenObtainPairView



# class LoginView(TokenObtainPairView):
#     """View for handling user authentication.
#     This view is responsible for authenticating a user using the provided email and password. If the provided
#     credentials are valid, the view returns a response with the user's authentication token. If the credentials are
#     invalid, the view returns a 400 Bad Request response with an error message indicating that the provided
#     credentials are incorrect.
#     """
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)

#             serializer.is_valid(raise_exception=True)  # Validate the serializer data
#             print(request.data)  # Debug statement to check the request data
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             serializer = self.get_serializer(data=request.data)
#             print(serializer.error)

#             try:
#                 user = User.objects.get(email=email)
#                 if not user.check_password(password):
#                     raise AuthenticationFailed('Invalid email or password.')

#                 if not user.is_active:
#                     raise AuthenticationFailed('Your account is not active.')
#             except User.DoesNotExist:
#                 raise AuthenticationFailed('Invalid email or password.')

#             response = super().post(request, *args, **kwargs)
#             responseData = {
#                 "Authorization": response.data,
#                 "user_data": serializer.data
#             }
#             response.data = BaseResponse(responseData, None, 'Login successful').to_dict()
#             return Response(response.data, status=status.HTTP_200_OK)
#         except AuthenticationFailed as e:
#             return abort(401, e.detail)  # Use e.detail directly

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

class UserLunchDashboard(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AllUserSerializer

    def get_queryset(self):
        return Users.objects.annotate(num_lunch=Count('lunch_reciever')).order_by('num_lunch')


class OTPRequestView(APIView):
    permission_classes = [AllowAny]

    def generate_otp(self, user):
        import random
        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        return otp
    
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp = self.generate_otp(user)
                email_subject = "Password Reset"
                message = f"Your OTP for password reset is: {otp}"
                from_email = "noreply@example.com"
                recipient_list = [email]

                # Send the OTP email
                send_mail(email_subject, message, from_email, recipient_list, fail_silently=False)
                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class OTPVerificationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.set_password(new_password)
                user.save()
                user.otp = None
                user.save()
                return Response({
                    "message": "success",
                    "message": "Password Reset Successful",
                    "status": status.HTTP_202_ACCEPTED,
                })
            else:
                return Response({
                    "message": "error",
                    "message": "Invalid OTP",
                    "status": status.HTTP_400_BAD_REQUEST,
                })
        return Response({
            "message": "error",
            "error": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST,
        })
