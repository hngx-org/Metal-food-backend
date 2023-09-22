from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Withdrawals
from .serializers import WithdrawalRequestSerializer, WithdrawalRequestGetSerializer
from users.models import Users


class WithdrawalRequestCreateView(generics.CreateAPIView):
    queryset = Withdrawals.objects.all()
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            bank_name=serializer.validated_data["bank_name"],
            bank_account=serializer.validated_data["bank_account"],
            bank_code=serializer.validated_data["bank_code"],
            amount=serializer.validated_data["amount"],
            
            withdrawal_request = Withdrawals.objects.create(
                amount=serializer.validated_data["amount"],
                user_id=request.user
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
        
        return self.create(request, *args, **kwargs)

class WithdrawalRequestListView(generics.ListAPIView):
    serializer_class = WithdrawalRequestGetSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        
        user = request.user
        
        if user is not None:
            try:
                user_id = Users.objects.get(id=user.id)
            except Users.DoesNotExist():
                response = {
                    "message": "User not found",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            queryset = Withdrawals.objects.all()
            serializer= WithdrawalRequestGetSerializer
            data= serializer(queryset, many=True).data
            
            response = {
                "message": "Withdrawal request retrieved successfully",
                "statusCode": status.HTTP_200_OK,
                "data": data
            }    
            return Response(response, status=status.HTTP_200_OK)
        
        else:
            response = {
                "message": "Used ID is required",
                "statusCode": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalRequestRetrieveView(generics.ListAPIView):
    serializer_class = WithdrawalRequestGetSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request,pk=None, *args, **kwargs):
        user = request.user
        
        if user is not None:

            try:
                user_id = Users.objects.get(id=user.id)
            except Users.DoesNotExist():
                response = {
                    "message": "User not found",
                    "statusCode": status.HTTP_404_NOT_FOUND,
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        
            if pk is not None:
                queryset = Withdrawals.objects.get(id=pk)
                data = WithdrawalRequestGetSerializer(queryset, many=False).data
                response = {
                    "message": "Withdrawal request retrieved successfully",
                    "statusCode": status.HTTP_200_OK,
                    "data": data
                }    
                return Response(response, status=status.HTTP_200_OK)
        
        else:
            response = {
                "message": "Used ID is required",
                "statusCode": status.HTTP_400_BAD_REQUEST,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


        
