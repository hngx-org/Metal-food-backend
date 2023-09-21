from rest_framework import serializers
from .models import Lunch


class LunchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lunch
        fields = '__all__'