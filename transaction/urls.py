from django.urls import path
from .views import WithdrawalRequestCreateView,SendLunchView,RedeemLunchView


urlpatterns = [
   path('/api/withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
   path('api/lunch/send',SendLunchView.as_view(),name='send-lunch'),
   path('api/lunch/redeem',RedeemLunchView.as_view(),name='redeem-lunch'),
]
