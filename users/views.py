from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from .models import Users


# Create your views here.

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def createuser(request):
#     try:
#         Users.objects.get(username = request.data['username'])
#         return Response("user already exists", status = status.HTTP_302_FOUND)
#     except Users.DoesNotExist:
#         serializer = UserSerializer(data = request.data)
#         serializer.password = make_password(request.data["password"])
#         if serializer.is_valid():
#             serializer.password = make_password(request.data["password"])
#             serializer.save()
#             return Response("User has been created", status= status.HTTP_201_CREATED)

#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    user = get_object_or_404(Users, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Object not Found"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user = user)
    serializer = UserSerializer(user, many= False)
    return Response({"token": token.key, "User": serializer.data })
    

