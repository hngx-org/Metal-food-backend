from rest_framework import serializers


class WithdrawalRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    bank_account = serializers.CharField(max_length=20)
    bank_name = serializers.CharField(max_length=50)
    bank_code = serializers.CharField(max_length=30)


class WithdrawalRequestGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    status = serializers.CharField(max_length=30)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField()

from .models import Lunch


class LunchSerializers(serializers.ModelSerializers):
    class Meta:
        model = Lunch
        fields = '__all__'

