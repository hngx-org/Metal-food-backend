from django.urls import path
from .views import WithdrawalRequestCreateView, SendLunchView, LunchDetailView
from . import views

urlpatterns = [
   # URL for sending lunch
   path('send-lunch/', SendLunchView.as_view(), name='send-a-lunch'),

   # URL for creating a withdrawal request
   path('withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),

   # URL for getting details of a single lunch (by its primary key)
   path('lunch/<str:pk>', LunchDetailView.as_view(), name='lunch-detail'),

   # URL for listing lunch history
   path('lunch/all/', views.ListLunchHistory.as_view(), name='list-lunch-history' ),

   # URL for redeeming a specific user's lunch (by its primary key)
   path('lunch/redeem/<str:pk>', views.RedeemLunch.as_view(), name='redeem-api-view')
]
