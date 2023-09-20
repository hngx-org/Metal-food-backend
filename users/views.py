from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import permissions
from .models import Users, Organization
from .serializers import UsersSerializer

class UsersListView(generics.ListAPIView):
    serializer_class = UsersSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        org_id = self.kwargs.get('org_id')
        queryset = Users.objects.filter(org_id=org_id)
        return queryset