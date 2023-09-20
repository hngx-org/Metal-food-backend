from django.urls import path 
from .views import UsersListView, UsersView

urlpatterns = [
    path('users/<int:org_id>/', UsersListView.as_view(), name='users-list'),
    path('users/signup/', UsersView.as_view(), name='users_signup'),
]
