from rest_framework import serializers
from .models import Users, Organization

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Organization
        fields = ['name' ,'lunch_price']
