from django.urls import path
from . import views

urlpatterns = [
   path('api/lunch/history', views.ListLunchHistory.as_view(), name='list-lunch-history' ),
]