from django.urls import path 
from .views import WithdrawalRequestCreateView, WithdrawalCountView
from . import views

urlpatterns = [
    path('withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
    path('withdrawal/count', WithdrawalCountView.as_view(), name='withdrawal_count'),
    path('api/lunch/history', views.ListLunchHistory.as_view(), name='list-lunch-history' ),
]
