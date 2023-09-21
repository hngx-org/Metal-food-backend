from django.urls import path
from .views import WithdrawalRequestCreateView, WithdrawalRequestGetView


urlpatterns = [
   path('api/withdrawal/request/', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
   path('api/withdrawat/get/', WithdrawalRequestGetView.as_view(), name="withdrawal_request_get_by_user")
]
