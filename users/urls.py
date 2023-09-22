from django.urls import path 
from . import views
from .views import UpdateOrganizationLunchWallet

urlpatterns = [
    path('api/user/all', views.ListUsersView.as_view(), name='list-users'),
    path('api/search/<str:nameoremail>/', views.SearchUserView.as_view(), name='search-user'),
    path('api/organization/<int:org_id>/wallet/update/', UpdateOrganizationLunchWallet.as_view()),
]