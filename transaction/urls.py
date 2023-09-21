from django.urls import path
from . import views

urlpatterns = [
   path('lunch/all/', views.ListLunchHistory.as_view(), name='list-lunch-history' ),
]