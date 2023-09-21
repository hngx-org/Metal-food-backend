from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import WithdrawalRequestSerializer, LunchSerializers, SendLunchSerializer, LunchDetailSerializer
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

            reciever_id = lunch.reciever_id #getting the user who owns the lunch
            try:
               reciever= Users.objects.get(id=reciever_id)
            except Users.DoesNotExist:
                reciever = None
                return Response({'message': 'Reciever does not exist', 'statusCode': status.HTTP_404_NOT_FOUND}, status= status.HTTP_404_NOT_FOUND)
            

            org_id= lunch.org_id #getting the orgarnization that gifted the lunch
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
    serializer_class = SendLunchSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Get the sender user
        sender = self.request.user

        # Validate sender's lunch credit balance
        lunch_credit_balance = sender.lunch_credit_balance
        quantity = serializer.validated_data["quantity"]

        if lunch_credit_balance < quantity:
            return Response(
                {"message": "Insufficient lunch credit balance", "statusCode": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deduct lunch credit from the sender's balance
        sender.lunch_credit_balance -= quantity
        sender.save()

        # Create the lunch instance with sender_id set to the current user
        serializer.save(sender_id=sender)

        return Response(
            {"message": "Lunch sent successfully", "statusCode": status.HTTP_201_CREATED},
            status=status.HTTP_201_CREATED,
        )



class LunchDetailView(generics.RetrieveAPIView):
    queryset = Lunch.objects.all()
    serializer_class = LunchDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)