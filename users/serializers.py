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
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

    def validate_username(self, value):
        # Check if a user with this username already exists
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value




class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'no_active_account': 'Your account is not active.',
        'invalid_credentials':'Invalid email or password.',
    }
