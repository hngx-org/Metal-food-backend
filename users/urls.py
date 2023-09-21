from django.urls import path 
Lunches
from .views import UsersListView

urlpatterns = [
    path('users/<int:org_id>/', UsersListView.as_view(), name='users-list'),
]

from .views import (
    OrganizationCreateAPIView,
    CreateInviteView,
    LoginView, RegisterUserView
)
from rest_framework_simplejwt.views import(
        TokenObtainPairView,
        TokenRefreshView,
        TokenVerifyView,
)


urlpatterns = [
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="refresh_view"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
        
    path('organization/create', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('organization/invite', CreateInviteView.as_view(), name='invite'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path("organization/staff/signup", RegisterUserView.as_view(), name="sign-up")
]
default
