from rest_framework import serializers
from .models import Users, Organization, OrganizationInvites
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from zeus import settings
from rest_framework.serializers import ModelSerializer
from .models import OrganizationLunchWallet


class GetOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'lunch_price']


class InviteSerializer(serializers.ModelSerializer):
    # organization = GetOrganizationSerializer(read_only=True)
    class Meta:
        model = OrganizationInvites
        fields = ['email',]

    def create(self, validated_data):
        """Create Invite"""
        token = self.context.get('token')
        user = self.context.get('request').user 
        org_id = user.org_id
        validated_data['token'] = token
        validated_data['org_id']= org_id
        invite = OrganizationInvites.objects.create(**validated_data)
        invite.save()
        return invite



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'organization', 'first_name', 'last_name', 'profile_pic', 'email', 'phone',
                  'is_admin', 'lunch_credit_balance', 'bank_number', 'bank_code', 'bank_name',
                  'currency', 'currency_code', 'created_at', 'updated_at', 'is_deleted']

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'bank_number', 'bank_code', 'bank_name']
        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        org = self.context.get('org')
        user = User(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            org=org
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    default_error_messages = {
        'no_active_account': 'Your account is not active.',
        'invalid_credentials':'Invalid email or password.',
    }


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    isAdmin = serializers.BooleanField(source="is_staff")
    
    class Meta:
        model = User
        fields = ["id", "name", "email", "profile_picture", "isAdmin"]
        
    def get_name(self, obj):
        """Joins first_name and last_name to get name"""
        return f"{obj.first_name} {obj.last_name}"
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            media_url = settings.MEDIA_URL
            return f"{media_url}{obj.profile_picture}"
        return None
    

class UserGetSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    user_id = serializers.CharField(source="id")
    
    class Meta:
        model = Users
        fields = ["name", "email", "profile_picture", "user_id"]
        
    def get_name(self, obj):
        """Joins first_name and last_name to get name"""
        return f"{obj.first_name} {obj.last_name}"
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            media_url = settings.MEDIA_URL
            return f"{media_url}{obj.profile_picture}"
        return None

class LunchWalletSerializer(ModelSerializer):
    class Meta:
        model = OrganizationLunchWallet
        fields = ('balance',)
        
class AllUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'profile_picture')
