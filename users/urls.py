from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('auth/user/signup', RegisterView.as_view(), name='user-signup')    
]