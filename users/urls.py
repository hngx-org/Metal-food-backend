from django.urls import path 
from .views import (
    OrganizationCreateAPIView,
    CreateInviteView
)

urlpatterns = [
    path('organization/create', OrganizationCreateAPIView.as_view(), name='create-organization'),
    path('organization/invite', CreateInviteView.as_view(), name='token_invite'),
]
