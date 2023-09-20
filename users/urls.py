from django.urls import path 
from .views import Login
urlpatterns = [
    # path('',createuser),
    path('Login/', Login)
]