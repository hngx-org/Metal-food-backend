from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Lunch
from .serializers import LunchSerializer


class ListLunchHistory(generics.ListAPIView):
    serializer_class = LunchSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]


    def get_queryset(self):
        user = self.request.user 
        query_set = Lunch.objects.filter(sender_id=user) | Lunch.objects.filter(receiver_id=user)
        return query_set     
