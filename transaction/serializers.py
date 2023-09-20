from rest_framework import serializers
from .models import Lunches



class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunches
        fields = '__all__'