from django.contrib.auth.hashers import make_password, BCryptSHA256PasswordHasher
from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        password = serializers.CharField(write_only=True)

        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'created_at', 'updated_at']


    def create(self, validated_data):
        """ 
        Hashing the password before saving
        """
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UsersSerializer, self).create(validated_data)
