from django.urls import path 
from .views import LoginView
from rest_framework_simplejwt.views import(
        TokenObtainPairView,
        TokenRefreshView,
        TokenVerifyView,
)


urlpatterns = [
        path("api/auth/login/", LoginView),
        path("jwt/create/", TokenObtainPairView.as_view(),
             name="jwt_create"),
        path("jwt/refresh/", TokenRefreshView.as_view(),
             name="refresh_view"),
        path("jwt/verify/", TokenVerifyView.as_view(),
             name="token_verify")
]
from django.urls import path

from .views import OrganizationCreateAPIView, CreateInviteView, LoginView

urlpatterns = [
    path('organization/create', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('organization/invite', CreateInviteView.as_view(), name='invite'),
    path('api/auth/login/', LoginView.as_view(), name='login')
]
