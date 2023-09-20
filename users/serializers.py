from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from  .models import Users, Organization


class GetOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'email',
            'lunch_price',
            'currency',
            'created_at',
            'password'
        ]
        # extra_kwargs = {
        #     "password": {"write_only":True, "required": True},
        # }

        def validate_password(self, value):
            """Validate password"""
            try:
                validate_password(value)
            except Exception as error:
                raise serializers.ValidationError(error.error_list)
            return value
        
        def create(self, validated_data):
            """Create Organization"""
            password = validate_password(validate_password.pop('password'))
            validated_data['password'] = make_password(password=password)
            organization = Organization.objects.create_user(**validated_data)
            organization.save()
            return organization

 


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True}}
        required_feilds = ['mobile']

    mobile = serializers.CharField(required=True)
    
    def create(self, validated_data):
        user = User(
          email=validated_data['email'],
          full_name=validated_data['full_name'],
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
