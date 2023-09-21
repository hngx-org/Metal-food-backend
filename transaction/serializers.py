from rest_framework import serializers
from .models import Lunch


class LunchSerializers(serializers.ModelSerializers):
    class Meta:
        model = Lunch
        fields = '__all__'