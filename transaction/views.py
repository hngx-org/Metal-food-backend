from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import WithdrawalRequestSerializer, LunchSerializers
from .models import Lunch, Withdrawals, Users
from users.models import Organization



class ListLunchHistory(generics.ListAPIView):
    serializer_class = LunchSerializers
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]


    def get_queryset(self):
        user = self.request.user 
        query_set = Lunch.objects.filter(sender_id=user) | Lunch.objects.filter(receiver_id=user)
        return query_set

    
class RedeemLunch(generics.GenericAPIView):
    serializer_class = LunchSerializers
    queryset = Lunch.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def put(reqeust, *args, **kwargs):
        lunch_id = kwargs.get('pk')
        if Lunch.objects.filter(id=lunch_id).exists():
            lunch = Lunch.objects.get(id= lunch_id)

            reciever_id = lunch.reciever_id#getting the user who owns the lunch
            try:
               reciever= Users.objects.get(id=reciever_id)
            except Users.DoesNotExist:
                reciever = None
                return Response({'message': 'Reciever does not exist', 'statusCode': status.HTTP_404_NOT_FOUND}, status= status.HTTP_404_NOT_FOUND)
            

            org_id= lunch.org_id#getting the orgarnization that gifted the lunch
            try: 
                org = Organization.objects.get(org_id=org_id)
            except Organization.DoesNotExist:
                org = None
                return Response({'message': 'Orgarnization does not exist', 'statusCode': status.HTTP_404_NOT_FOUND}, status= status.HTTP_404_NOT_FOUND)


            if reciever is not None and org is not None:
                lunch_quantity = int(lunch.quantity)
                org_lunch_price = org.lunch_price

                reward = lunch_quantity * org_lunch_price #quantity of lunch multiply by price of one lunch
                reciever.lunch_credit_balance += reward #increasing the users lunch credit balance
                lunch.redeemed = True #lunch has been redeemed
                reciever.save()
                lunch.save()
                return Response({
                    'message': 'Lunch request created successfully',
                    'statusCode': status.HTTP_201_CREATED,
                    'data': {
                        'lunch_credit_balance': reciever.lunch_credit_balance,
                        'first_name': reciever.first_name,
                        'last_name': reciever.last_name
                    }
                })
                 
        else:
            return Response({
                'message': 'Lunch not found',
                'statusCode': status.HTTP_404_NOT_FOUND
            }, status= status.HTTP_404_NOT_FOUND)

class GetALunch(generics.RetrieveAPIView):
    queryset = Lunch.objects.all()
    serializer_class = LunchSerializers
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        lunch_id = kwargs.get('pk')
        try:
            lunch = Lunch.objects.get(id= lunch_id)
        except Lunch.DoesNotExist:
            lunch = None
            return Response({'message': 'Lunch does not exist'})
        
        if lunch is not None:
            context = {
                'message': 'Lunch found',
                'statusCode': status.HTTP_200_OK,
                'data': lunch
            }

            return Response(context, status=status.HTTP_200_OK)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset()
    

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
