from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Withdrawals,Lunches
from .serializers import WithdrawalRequestSerializer,LaunchSerializerPost


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
class SendLunchView(generics.CreateAPIView):
    serializer_class = LaunchSerializerPost
    queryset = Lunches.objects.all()
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            senderId=request.user
            note=serializer.validated_data.get('note')
            for receiver_Id in serializer.validated_data.get('receiverId'):
                receiverId=receiver_Id['id']
                quantity=receiver_Id['quantity']
                Lunches.objects.create(sender_id=senderId, reciever_id=int(receiverId), quantity=quantity, note=note)
            return Response({"message": "Lunches created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)