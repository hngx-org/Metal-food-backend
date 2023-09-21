from django.urls import path
from . import views


urlpatterns = [
   path('api/withdrawal/request', views.WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
   path('api/withdrawal/get', views.WithdrawalRequestListView.as_view(), name="withdrawal_request_get_by_user"),
   path('api/withdrawal/get/<int:pk>', views.WithdrawalRequestRetrieveView.as_view(), name="withdrawal_request_detail_get_by_user"),
]
