from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LunchWalletSerializer
from .models import OrganizationLunchWallet

class UpdateOrganizationLunchWallet(APIView):

    """
    Title: Update Organization launch wallet balance
    Description: Description: Allows an admin user to update wallet balance.

    Endpoint: /api/organization/wallet/update
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