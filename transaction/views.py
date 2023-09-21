from decimal import Decimal
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

    def post(self, request, *args, **kwargs):
        serializer = WithdrawalRequestSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            withdrawal_amount=serializer.validated_data.pop("amount")
            withdrawal_amount = Decimal(withdrawal_amount)
            withdrawal_staus='success'
            instance = serializer.save(amount=withdrawal_amount,status=withdrawal_staus)
            withdrawals_data = {
                "id": instance.pk,
                #add this when authentication is complete
                #"user_id": instance.user_id,
                "status": instance.status,
                "amount": instance.amount,
                "created_at": instance.created_at.isoformat()
            }
            response_data = {
                "message": "Withdrawal request created successfully",
                "statusCode": status.HTTP_201_CREATED,
                "data": withdrawals_data 
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return self.create(request, *args, **kwargs)

class WithdrawalRequestListView(generics.ListAPIView):
    serializer_class = WithdrawalRequestGetSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        #change the request.user to request.GET.get("user_id", None)
        user = request.user
        
        if user is not None:
            #add this when authentication is complete
            # try:
            #     user = Users.objects.get(id=user_id)
            # except Users.DoesNotExist():
            #     response = {
            #         "message": "User not found",
            #         "statusCode": status.HTTP_404_NOT_FOUND,
            #     }
            #     return Response(response, status=status.HTTP_404_NOT_FOUND)
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
      #change the request.user to request.GET.get("user_id", None)
        user = request.user
        
        if user is not None:
            #add this when authentication is complete

            # try:
            #     user = Users.objects.get(id=user_id)
            # except Users.DoesNotExist():
            #     response = {
            #         "message": "User not found",
            #         "statusCode": status.HTTP_404_NOT_FOUND,
            #     }
            #     return Response(response, status=status.HTTP_404_NOT_FOUND)
        
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


# class WithdrawalRequestGetView(generics.RetrieveAPIView):
#     serializer_class = WithdrawalRequestGetSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, *args, **kwargs):
#         user_id = request.GET.get("user_id", None)
        
#         if user_id is not None and user_id != "":
#             try:
#                 user = Users.objects.get(id=user_id)
#             except Users.DoesNotExist():
#                 response = {
#                     "message": "User not found",
#                     "statusCode": status.HTTP_404_NOT_FOUND,
#                 }
#                 return Response(response, status=status.HTTP_404_NOT_FOUND)
        
#             queryset = Withdrawals.objects.filter(user_id=user_id)
#             serializer = self.get_serializer(queryset, many=True)
            
#             response = {
#                 "message": "Withdrawal request retrieved successfully",
#                 "statusCode": status.HTTP_200_OK,
#                 "data": serializer.data
#             }    
#             return Response(response, status=status.HTTP_200_OK)
        
#         else:
#             response = {
#                 "message": "Used ID is required",
#                 "statusCode": status.HTTP_400_BAD_REQUEST,
#             }
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
