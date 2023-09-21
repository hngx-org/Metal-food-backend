from rest_framework import serializers
from.models import Withdrawals

class WithdrawalRequestSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(max_length=50)
    bank_code = serializers.CharField(max_length=30)
    bank_account = serializers.CharField(max_length=20)
    status=serializers.CharField(read_only = True)

    class Meta:
        model = Withdrawals
        fields = ['pk','amount' ,'status','bank_name', 'bank_code', 'bank_account']

    def create(self, validated_data):
       
        bank_name = validated_data.pop('bank_name')
        bank_code = validated_data.pop('bank_code')
        bank_account = validated_data.pop('bank_account')
  
        withdrawals = Withdrawals.objects.create(**validated_data)

        return withdrawals


class WithdrawalRequestGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Withdrawals
        fields = ['pk','status','amount','created_at']