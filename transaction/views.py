from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Lunches
from users.models import Organization

# Create your views here.


class GetALunch(generics.RetrieveAPIView):
    queryset = Lunches.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        lunch_id = kwargs.get('pk')
        try:
            lunch = Lunches.objects.get(id= lunch_id)
        except Lunches.DoesNotExist:
            lunch = None
            return Response({'message': 'Lunch does not exist'})
        
        if lunch is not None:
            lunch_dict = {
                'id': lunch.id,
                'sender_id': lunch.sender_id.id,
                'receiver_id': lunch.reciever_id.id,
                'quantity': lunch.quantity,
                'redeemed': lunch.redeemed,
                'note': lunch.note,
                'created_at': lunch.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Convert DateTimeField to string
            }
            context = {
                'message': 'Lunch found',
                'statusCode': status.HTTP_200_OK,
                'data': lunch_dict
            }

            return Response(context, status=status.HTTP_200_OK)
        return super().get(request, *args, **kwargs)

class UpdateOrgLunchPrice(generics.UpdateAPIView):
    queryset = Organization.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication]

    def update(self, request, *args, **kwargs):
        org = Organization.objects.first()#We are instructed to work with only one orgarnization
        new_lunch_price = request.data.get('lunch_price')
        if org is not None:
            org.lunch_price = new_lunch_price
            org.save()
            context = {
                'message': 'success',
                'statusCode': status.HTTP_200_OK,
                'lunch_price': org.lunch_price
            }
            return Response(context, status=status.HTTP_200_OK)
        
        return Response({'message': 'Orgarnization not found'},  status=status.HTTP_404_NOT_FOUND)
