from django.contrib.auth.backends import ModelBackend
from users.models import Users, Organization
from rest_framework import serializers
# from django.contrib import sessions


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, **credentials):
        print("ggrg")
        email = credentials.get('email')
        password = credentials.get('password')

        if email and password:
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                print("Not User")
                try:
                    user = Organization.objects.get(email=email)
                except Organization.DoesNotExist:
                    print('Not Organization')
                    return None
            print(user)
            if not self.user_can_authenticate(user):
                raise serializers.ValidationError("Account not active!")
            print("Can Authenticate")
            print(password)           
            
            if user.check_password(password) and self.user_can_authenticate(user):
                print(user)
                return user
