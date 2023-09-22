from rest_framework.serializers import ModelSerializer
from .models import OrganizationLunchWallet


class LunchWalletSerializer(ModelSerializer):
    class Meta:
        model = OrganizationLunchWallet
        fields = ('balance',)