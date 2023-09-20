from django.urls import path 
from .views import *

urlpatterns = [
   path('/api/withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request")
]
