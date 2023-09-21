from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'organization', 'first_name', 'last_name', 'profile_pic', 'email', 'phone',
                  'is_admin', 'lunch_credit_balance', 'bank_number', 'bank_code', 'bank_name',
                  'currency', 'currency_code', 'created_at', 'updated_at', 'is_deleted']

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['bank_number', 'bank_code', 'bank_name']