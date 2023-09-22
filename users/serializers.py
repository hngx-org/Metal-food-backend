from rest_framework.serializers import ModelSerializer
from .models import OrganizationLunchWallet, Users


class LunchWalletSerializer(ModelSerializer):
    class Meta:
        model = OrganizationLunchWallet
        fields = ('balance',)
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'profile_picture')