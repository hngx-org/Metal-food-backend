from django.urls import path
from .views import WithdrawalRequestCreateView
from . import views

urlpatterns = [
   path('/api/withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
   path('lunch/all/', views.ListLunchHistory.as_view(), name='list-lunch-history' ),
   path('lunch/redeem/<str:pk>', views.RedeemLunch.as_view(), name='redem-api-view'),
   path('lunch/<str:pk>', views.GetALunch.as_view(), name='getalunch')
]
