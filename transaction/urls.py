from django.urls import path 
from .views import ListLunchHistory

urlpatterns = [
    path('/lunches/', ListLunchHistory.as_view(), name='user-lunch-history')
]