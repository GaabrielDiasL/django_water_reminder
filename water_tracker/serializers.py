from rest_framework import serializers
from .models import User, WaterIngested

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'weight', 'daily_target']

class WaterIngestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIngested
        fields = ['id', 'user', 'amount_ml', 'date']