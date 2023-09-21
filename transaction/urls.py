from django.urls import path
from . import views

urlpatterns = [
   path('api/lunch/all', views.GetAllLunch.as_view(), name='get-all-lunch' ),
]