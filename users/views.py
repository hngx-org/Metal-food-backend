from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Users, Organization
from .serializers import UsersSerializer

class UsersListView(generics.ListAPIView):
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        org_id = self.kwargs.get('org_id')
        queryset = Users.objects.filter(org_id=org_id)
        return queryset
    

class UsersView(APIView):
    def post(self, request):
        """ 
        Create a new user
        """
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "message": "User created successfully!",
                "code": 201,
                "data":serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(data={
            "message":serializer.errors,
            "code":400,
            "data":{}
        }, status=status.HTTP_400_BAD_REQUEST)
