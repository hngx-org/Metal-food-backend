from rest_framework import serializers
from .models import Lunch


class LunchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = '__all__'



class WithdrawalRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    bank_account = serializers.CharField(max_length=20)
    bank_name = serializers.CharField(max_length=50)
    bank_code = serializers.CharField(max_length=30)



class WithdrawalCountSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    withdrawal_count =serializers.IntegerField()


#create serializer here