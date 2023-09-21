from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Withdrawals,Lunches
from .serializers import WithdrawalRequestSerializer,LaunchSerializerPost
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication

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
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    queryset = Lunches.objects.all()
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        user = Users.objects.get(id=request.user.id)
        request_data = request.data.copy()
        request_data['senderId'] = request.user.id
        serializer=self.get_serializer(data=request_data)
        if serializer.is_valid():
            senderId=request.user.id
            note = serializer.validated_data.get('note')
            quantity=serializer.validated_data.get('quantity')
            for receiver_Id in serializer.validated_data.get('receivers'):
                Lunches.objects.create(sender_id=senderId, reciever_id=receiver_Id, quantity=quantity, note=note)
            return Response({ "message": "Lunch request created successfully","data": {}}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)