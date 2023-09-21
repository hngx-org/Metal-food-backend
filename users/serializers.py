from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Organization, OrganizationInvites


class GetOrganizationSetializer(serializers.ModelSerializer):
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

        # extra_kwargs = {'password': {'write_only': True}}

        def check_password(self, value):
            """Validate password"""
            try:
                validate_password(value)
            except Exception as error:
                raise ValidationError(error.error_list)
            return value
        
        def create(self, validated_data):
            """Create Organization"""
            password = self.check_password(validated_data.pop('password'))
            email = validated_data.pop('email')
            organization = Organization.objects.create_user(email, password, **validated_data)
            return organization
        

class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationInvites
        fields = ['org_id', 'email']

    def create(self, validated_data):
        """Create Invite"""
        token = self.context.get('token')
        validated_data['token'] = token
        invite = OrganizationInvites.objects.create(**validated_data)
        invite.save()
        return invite