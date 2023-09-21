<<<<<<< HEAD
=======

>>>>>>> 640ac28cc52c2e7d74e60999052cfd4dbe0240be
from django.urls import path 
from .views import WithdrawalRequestCreateView, WithdrawalCountView
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
    path('withdrawal/count', WithdrawalCountView.as_view(), name='withdrawal_count'),
    path('api/lunch/history', views.ListLunchHistory.as_view(), name='list-lunch-history' ),
=======
   path('withdrawal/request', WithdrawalRequestCreateView.as_view(), name="withdrawal_request"),
   path('withdrawal/count', WithdrawalCountView.as_view(), name='withdrawal_count'),
   path('api/lunch/history', views.ListLunchHistory.as_view(), name='list-lunch-history' ),
>>>>>>> 640ac28cc52c2e7d74e60999052cfd4dbe0240be
]
