from django.urls import path 

urlpatterns = [
   path('/api/withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request")
]
