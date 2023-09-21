from django.urls import path 
from . import views
urlpatterns = [
    path('api/user/all', views.ListUsersView.as_view(), name='list-users'),
    path('api/search/<str:nameoremail>/', views.SearchUserView.as_view(), name='search-user'),
]