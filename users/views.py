from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Users
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LunchWalletSerializer, UserSerializer
from .models import OrganizationLunchWallet

class UpdateOrganizationLunchWallet(APIView):

    """
    Title: Update Organization launch wallet balance
    Description: Description: Allows an admin user to update wallet balance.

    Endpoint: /api/<id>/organization/wallet/update
    Method:PATCH
    """
    queryset = OrganizationLunchWallet.objects.all()

    def patch(self, request, org_id):
        wallet = OrganizationLunchWallet.objects.get(org_id=org_id)
        serializer = LunchWalletSerializer(wallet, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "success",
                "status": 200,
                "data": serializer.data
            })
        return Response({
            "message": "error",
            "error": serializer.errors
        })
        

class ListUsersView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class SearchUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        nameoremail = self.kwargs.get('nameoremail')  # Get the nameoremail parameter from the URL
        # Perform a case-insensitive search on first_name, last_name, and email
        queryset = Users.objects.filter(
            Q(first_name__icontains=nameoremail) |
            Q(last_name__icontains=nameoremail) |
            Q(email__icontains=nameoremail)
        )
        return queryset

    def retrieve(self, request, nameoremail):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset)
        serializer = UserSerializer(user)
        return Response({
            "message": "User found",
            "statusCode": status.HTTP_200_OK,
            "data": serializer.data
        })