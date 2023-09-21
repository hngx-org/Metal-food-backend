from django.urls import path 
from .views import UsersListView, CreateOrganization

# UsersListView,

urlpatterns = [
    path('api/organization/create', CreateOrganization.as_view(), name='create-organization'),
    path('<int:org_id>/', UsersListView.as_view(), name='users-list'),
    path('', UsersListView.as_view(), name='users-list'),
]
