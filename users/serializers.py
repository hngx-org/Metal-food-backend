from .models import Users, Organization, OrganizationInvites
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'username', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        org = self.context.get('org')
        user = Users(
            email=validated_data['email'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            username=validated_data['username'],
            org=org
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

    def validate_username(self, value):
        # Check if a user with this username already exists
        if Users.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value


class LoginSerializer(TokenObtainPairSerializer):
    """
    Handles login serializer
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'no_active_account': 'Your account is not active.',
        'invalid_credentials':'Invalid email or password.',
    }