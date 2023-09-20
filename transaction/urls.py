from django.urls import path
from .views import WithdrawalRequestCreateView,SendLunchView


urlpatterns = [
   path('/api/withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
   path('api/lunch/send',SendLunchView.as_view(),name='send-lunch'),
]
