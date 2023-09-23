from django.urls import path 
from .views import WithdrawalRequestCreateView, WithdrawalCountView, SendLunchView, RedeemLunchView, ListLunchHistory, ListAllLunches, LunchDetailView
from . import views

urlpatterns = [
   path('withdrawal/request/', WithdrawalRequestCreateView.as_view(), name='withdrawal_request'),
   path('withdrawal/count/', WithdrawalCountView.as_view(), name='withdrawal_count'),
   path('lunch/history/',ListLunchHistory.as_view(), name='list-lunch-history' ),
   path('lunch/send/',SendLunchView.as_view(),name='send-lunch'),
   path('lunch/redeem/',RedeemLunchView.as_view(),name='redeem-lunch'),
   path('lunch/all/', ListAllLunches.as_view(), name='list-all-lunches'),
   path('withdrawal/get', views.WithdrawalRequestListView.as_view(), name="withdrawal_request_get_by_user"),
   path('withdrawal/get/<int:pk>', views.WithdrawalRequestRetrieveView.as_view(), name="withdrawal_request_detail_get_by_user"),
   path('lunch/<str:pk>', LunchDetailView.as_view(), name='lunch-detail'),
]
