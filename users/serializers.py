from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from  .models import Users
 


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'mobile']
        extra_kwargs = {'password': {'write_only': True}}
        required_feilds = ['mobile']

    mobile = serializers.CharField(required=True)
    
    def create(self, validated_data):
        user = User(
          email=validated_data['email'],
          full_name=validated_data['full_name'],
          mobile=validated_data['mobile']
          )
        user.set_password(validated_data['password'])
        user.is_active = False  
        
    
        user.save()
        return user



class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'no_active_account': 'Your account is not active.',
        'invalid_credentials':'Invalid email or password.',
    }
