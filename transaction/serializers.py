from rest_framework import serializers
from.models import Withdrawals

class WithdrawalRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    bank_number = serializers.CharField(max_length=20)
    bank_name = serializers.CharField(max_length=50)
    bank_code = serializers.CharField(max_length=30)

class WithdrawalRequestGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Withdrawals
        fields = ['pk','status','amount','created_at']