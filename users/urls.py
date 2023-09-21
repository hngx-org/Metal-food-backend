from django.urls import path 
from .views import UpdateOrganizationLunchWallet

urlpatterns = [
    path('api/organization/<int:org_id>/wallet/update/', UpdateOrganizationLunchWallet.as_view()),
]