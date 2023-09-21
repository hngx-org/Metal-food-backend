from django.urls import path 
from . import views

urlpatterns = [
     path('api/lunch/<str:pk>', views.GetALunch.as_view(), name='getalunch'),
     path('api/organization/launch/update/', views.UpdateOrgLunchPrice.as_view(), name='updateorglunchprice')
]