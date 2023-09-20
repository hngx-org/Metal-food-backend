from django.urls import path 
from .views import UsersView


urlpatterns = [
   path("api/organization/staff/signup/",UsersView.as_view())
]