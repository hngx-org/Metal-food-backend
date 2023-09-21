from rest_framework import serializers
Lunches
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']



from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from  .models import Users, Organization, OrganizationInvites


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


class InviteSerializer(serializers.ModelSerializer):
    # organization = GetOrganizationSerializer(read_only=True)
    class Meta:
        model = OrganizationInvites
        fields = ['org_id', 'email',]

    def create(self, validated_data):
        """Create Invite"""
        token = self.context.get('token')
        validated_data['token'] = token
        validated_data['org_id']= validated_data.get('org_id')
        invite = OrganizationInvites.objects.create(**validated_data)
        invite.save()
        return invite



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        org = self.context.get('org')
        user = User(
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
default
