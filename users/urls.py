from django.urls import path 
from .views import UsersListView

urlpatterns = [
    path('<int:org_id>/', UsersListView.as_view(), name='users-list'),
]
