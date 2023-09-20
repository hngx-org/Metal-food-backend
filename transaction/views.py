from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import WithdrawalRequestSerializer, LunchSerializers
from .models import Lunch, Withdrawals, Users



class ListLunchHistory(generics.ListAPIView):
    serializer_class = LunchSerializers
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]


    def get_queryset(self):
        user = self.request.user 
        query_set = Lunch.objects.filter(sender_id=user) | Lunch.objects.filter(receiver_id=user)
        return query_set


class RedeemUserLunch(generics.UpdateAPIView):
    serializer_class = LunchSerializers
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]
    queryset = Lunch.objects.all()
    lookup_field= 'pk'

    def get_queryset(self):
        


        return super().get_queryset()

    def perform_update(self, serializer):
        lunch_id = self.kwargs.get('pk')
        print('the linch is', lunch_id)
        return super().perform_update(serializer)
    
class RedeemLunch(generics.GenericAPIView):
    serializer_class = LunchSerializers
    queryset = Lunch.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def put(reqeust, *args, **kwargs):
        lunch_id = reqeust.kwargs.get('pk')
        if Lunch.objects.filter(id=lunch_id).exists():
            lunch = Lunch.objects.get(id= lunch_id)

            reciever_id = lunch.reciever_id
            #get reciever and credit them
            # lunch.redeemed = True        
        
        return Response({'message': lunch_id})



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
