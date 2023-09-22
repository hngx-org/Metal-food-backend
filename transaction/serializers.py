from rest_framework import serializers
from .models import Lunch
from users.models import Users
from django.shortcuts import get_object_or_404


class LunchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = "__all__"


class WithdrawalRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    bank_account = serializers.CharField(max_length=20)
    bank_name = serializers.CharField(max_length=50)
    bank_code = serializers.CharField(max_length=30)


class WithdrawalCountSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    withdrawal_count = serializers.IntegerField()


class LaunchSerializerPost(serializers.Serializer):
    quantity = serializers.IntegerField()
    note = serializers.CharField(required=False, allow_blank=True)
    receivers = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all(), many=True
    )

    def validate_quantity(self, value):
        if int(value) < 1:
            raise serializers.ValidationError("Lunch given should be above 0")
        else:
            return value

    def validate(self, data):
        sender_Id = self.context["senderId"]
        if sender_Id in data["receivers"]:
            raise serializers.ValidationError("You can't send lunch to yourself")
        else:
            return data


class RedeemSerialize(serializers.Serializer):
    id = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def validate(self, data):
        for lunch_id in data["id"]:
            lunch = get_object_or_404(Lunch, id=lunch_id)
            if lunch.redeemed == True:
                raise serializers.ValidationError("Lunch already redeemed")
        return data
