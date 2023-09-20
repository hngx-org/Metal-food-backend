from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, hashers
from  .models import Users
 


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}



class StaffRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password',]
        # extra_kwargs = {'password': {'write_only': True}}
        # required_feilds = ['mobile']

    # mobile = serializers.CharField(required=True)
    
    def create(self, validated_data):
        validated_data['password'] = hashers.make_password(validated_data.get('password'))
        return super(StaffRegisterSerializer, self).create(validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'no_active_account': 'Your account is not active.',
        'invalid_credentials':'Invalid email or password.',
    }
