from django.urls import path 
from .views import WithdrawalRequestCreateView, WithdrawalCountView, SendLunchView, RedeemLunchView, ListLunchHistory
from . import views

urlpatterns = [
   path('withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
   path('withdrawal/count', WithdrawalCountView.as_view(), name='withdrawal_count'),
   path('api/lunch/history',ListLunchHistory.as_view(), name='list-lunch-history' ),
   path('api/lunch/send',SendLunchView.as_view(),name='send-lunch'),
   path('api/lunch/redeem',RedeemLunchView.as_view(),name='redeem-lunch'),
]
