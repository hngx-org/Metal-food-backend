from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import permissions
from .models import Users, Organization
from .serializers import UsersSerializer
from django.db.models import Q

class UsersListView(generics.ListAPIView):
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        org_id = self.kwargs.get('org_id', None)
        if org_id:
            queryset = Users.objects.filter(org_id=org_id)
        else:
            queryset = Users.objects.all()
        search = self.request.GET.get('search', '')
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
        return queryset