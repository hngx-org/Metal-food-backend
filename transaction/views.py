from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Withdrawals
from .serializers import WithdrawalRequestSerializer, WithdrawalRequestGetSerializer
from users.models import Users


class WithdrawalRequestCreateView(generics.CreateAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            withdrawal_request = Withdrawals.objects.create(
                bank_name=serializer.validated_data["bank_name"],
                bank_number=serializer.validated_data["bank_number"],
                bank_code=serializer.validated_data["bank_code"],
                amount=serializer.validated_data["amount"],
                user=request.user
            )

            withdrawal_request.status = "success"
            withdrawal_request.save()

            response_data = {
                "message": "Withdrawal request created successfully",
                "statusCode": status.HTTP_201_CREATED,
                "data": {
                    "id": withdrawal_request.id,
                    "user_id": withdrawal_request.user_id,
                    "status": withdrawal_request.status,
                    "amount": withdrawal_request.amount,
                    "created_at": withdrawal_request.created_at.isoformat()
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)


class WithdrawalRequestGetView(generics.RetrieveAPIView):
    serializer_class = WithdrawalRequestGetSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get("user_id", None)
        
        if user_id is not None and user_id != "":
            try:
                user = Users.objects.get(id=user_id)
            except Users.DoesNotExist():
                response = {
                    "message": "User not found",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        
            queryset = Withdrawals.objects.filter(user_id=user_id)
            serializer = self.get_serializer(queryset, many=True)
            
            response = {
                "message": "Withdrawal request retrieved successfully",
                "statusCode": status.HTTP_200_OK,
                "data": serializer.data
            }    
            return Response(response, status=status.HTTP_200_OK)
        
        else:
            response = {
                "message": "Used ID is required",
                "statusCode": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
