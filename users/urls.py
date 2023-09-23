from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('add-bank-account/', AddBankAccountView.as_view(), name='add-bank-account'),
    # path("auth/login", TokenObtainPairView.as_view(), name="jwt_create"),
    # path("jwt/refresh/", TokenRefreshView.as_view(), name="refresh_view"),
    # path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('auth/login', LoginView.as_view(), name='login'),
    
    path('organization/create/', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('organization/invite/', CreateInviteView.as_view(), name='token_invite'),
    
    path("organization/admin/signup/", RegisterUSERView.as_view(), name="sign-up-admin"),
    path("organization/staff/signup/", RegisterSTAFFView.as_view(), name="sign-up"),
    path('organization/<int:org_id>/wallet/update/', UpdateOrganizationLunchWallet.as_view()),
        
    path('all/', ListUsersView.as_view(), name='list-users'),
    path('search/<str:nameoremail>/', SearchUserView.as_view(), name='search-user'),
    path('profile/', UserRetrieveView.as_view(), name="retrieve-user"),
    path('lunch/leaderboard/', UserLunchDashboard.as_view(), name='leaderboard'),
    path('otp-verification/', OTPVerificationView.as_view(), name='otp-verification'),
]
