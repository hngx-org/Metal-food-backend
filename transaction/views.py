from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Withdrawals,Lunch
from .serializers import LunchSerializers,WithdrawalCountSerializer,LaunchSerializerPost,RedeemSerialize, WithdrawalRequestSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from users.models import Users
from django.shortcuts import get_object_or_404

class ListLunchHistory(generics.ListAPIView):
    serializer_class = LunchSerializers
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def get_queryset(self):
        user = self.request.user 
        query_set = Lunch.objects.filter(sender_id=user) | Lunch.objects.filter(receiver_id=user)
        return query_set 


        """
        Get the count of withdrawal made by user
        """
class WithdrawalCountView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        #  count of withdrawal requests for the user
        withdrawal_count = Withdrawals.objects.filter(user=request.user).count()
        serializer = WithdrawalCountSerializer({
            "user_id": request.user.id,
            "withdrawal_count": withdrawal_count,
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
class SendLunchView(generics.CreateAPIView):
    serializer_class = LaunchSerializerPost
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    queryset = Lunch.objects.all()
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data,context={'senderId':Users.objects.get(id=request.user.id)})
        print(request.user.id)
        if serializer.is_valid():
            senderId = Users.objects.get(id=request.user.id)
            note = serializer.validated_data.get('note')
            quantity=serializer.validated_data.get('quantity')
            for receiver_Id in serializer.validated_data.get('receivers'):
                Lunch.objects.create(sender_id=senderId, reciever_id=receiver_Id, quantity=quantity, note=note)
            return Response({ "message": "Lunch request created successfully","data": {}}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RedeemLunchView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = RedeemSerialize(data=request.data)
        if serializer.is_valid(raise_exception=True):
            for lunchId in serializer.validated_data.get('id'):
                lunch=Lunch.objects.get(id=lunchId)
                lunch_credit=lunch.quantity
                lunch.redeemed=True
                receiver=get_object_or_404(Users,first_name=lunch.reciever_id.first_name)
                receiver.lunch_credit_balance +=lunch_credit
                lunch.save()
                receiver.save()
            return Response({ "message": "success",  "statusCode": 200,"data": "null"})


class WithdrawalRequestCreateView(generics.CreateAPIView):
    queryset = Withdrawals.objects.all()
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
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


class ListAllLunches(generics.ListAPIView):
    serializer_class = LunchSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def get_queryset(self):
        queryset = Lunch.objects.all()
        return queryset