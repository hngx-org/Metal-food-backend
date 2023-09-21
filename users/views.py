from django.shortcuts import render

# Create your views here.
from rest_framework import generics,status
from rest_framework import permissions
from rest_framework.response import Response
from .models import Users, Organization
from .serializers import UsersSerializer, OrganizationSerializer
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
      

class CreateOrganization(generics.GenericAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(request.user)
        data = request.data 
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
