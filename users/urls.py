from django.urls import path
from .views import AddBankAccountView
 

urlpatterns = [
    path('api/user/add-bank-account', AddBankAccountView.as_view(), name='add-bank-account'),
]