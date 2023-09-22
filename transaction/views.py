from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Withdrawals
from .serializers import WithdrawalRequestSerializer, WithdrawalRequestGetSerializer
from users.models import Users


class WithdrawalRequestCreateView(generics.CreateAPIView):
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
                # user_id=request.user, 
                user_id=1,
                status="pending",
                amount=amount,
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
        

from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Lunch
from .serializers import LunchSerializers


class ListLunchHistory(generics.ListAPIView):
    serializer_class = LunchSerializers
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]


    def get_queryset(self):
        user = self.request.user 
        query_set = Lunch.objects.filter(sender_id=user) | Lunch.objects.filter(receiver_id=user)
        return query_set     

