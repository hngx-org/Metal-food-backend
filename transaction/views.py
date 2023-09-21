from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Lunch, Withdrawals
from .serializers import LunchSerializers  #, WithdrawalCountSerializer


class GetAllLunch(generics.ListAPIView):
    serializer_class = LunchSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def get_queryset(self):
        user = self.request.user 
        query_set = Lunch.objects.filter(sender_id=user) | Lunch.objects.filter(receiver_id=user)
        return query_set 


        """
        Get the count of withdrawal made by user
        """
# class WithdrawalCountView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         #  count of withdrawal requests for the user
#         withdrawal_count = Withdrawals.objects.filter(user=request.user).count()
#         serializer = WithdrawalCountSerializer({
#             "user_id": request.user.id,
#             "withdrawal_count": withdrawal_count,
#         })

#         return Response(serializer.data, status=status.HTTP_200_OK)