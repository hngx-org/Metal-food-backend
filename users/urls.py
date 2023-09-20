from django.urls import path

from .views import OrganizationCreateAPIView

urlpatterns = [
    path('organization/create', OrganizationCreateAPIView.as_view(), name='create-organization'),
]