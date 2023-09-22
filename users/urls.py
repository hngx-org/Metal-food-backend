from django.urls import path 
from .views import *

from rest_framework_simplejwt.views import(
        TokenObtainPairView,
        TokenRefreshView,
        TokenVerifyView,
)


urlpatterns = [
     path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
     path("jwt/refresh/", TokenRefreshView.as_view(), name="refresh_view"),
     path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
     path('auth/login', LoginView.as_view(), name='login'),
     path('auth/logout', LogoutView.as_view(),name='logout'),
     
    
     path("organization/staff/signup", RegisterUserView.as_view(), name="sign-up")

]