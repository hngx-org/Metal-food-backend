from django.urls import path 
from .views import WithdrawalRequestCreateView, WithdrawalCountView

urlpatterns = [
    path('withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
    path('withdrawal/count', WithdrawalCountView.as_view(), name='withdrawal_count'),
]
