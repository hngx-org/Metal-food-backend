from rest_framework import serializers
from users.models import Users
class WithdrawalRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    bank_account = serializers.CharField(max_length=20)
    bank_name = serializers.CharField(max_length=50)
    bank_code = serializers.CharField(max_length=30)
class LaunchReceiverSerializersPost(serializers.Serializer):
    receiverId=serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    quantity=serializers.IntegerField()
class LaunchSerializerPost(serializers.Serializer):
    receivers=LaunchReceiverSerializersPost(many=True)
    senderId=serializers.IntegerField()
    note=serializers.CharField(required=False, allow_blank=True)