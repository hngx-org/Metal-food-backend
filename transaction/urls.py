from django.urls import path
from .views import WithdrawalRequestCreateView


urlpatterns = [
   path('withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request")

]
