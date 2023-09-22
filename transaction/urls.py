from django.urls import path
from .views import SendLunchView,RedeemLunchView,ListLunchHistory

urlpatterns = [
   path('api/lunch/history',ListLunchHistory.as_view(), name='list-lunch-history' ),
   path('api/lunch/send',SendLunchView.as_view(),name='send-lunch'),
   path('api/lunch/redeem',RedeemLunchView.as_view(),name='redeem-lunch'),
]