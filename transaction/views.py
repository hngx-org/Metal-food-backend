from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Lunches
from .serializers import LunchSerializer


class ListLunchHistory(generics.ListAPIView):
    serializer_class = LunchSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]


    def get_queryset(self):
        user = self.request.user 
        query_set = Lunches.objects.filter(sender_id=user) | Lunches.objects.filter(receiver_id=user)
        return query_set
