from rest_framework import serializers
from .models import User, WaterIngested, CupSize

class CupSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CupSize
        fields = ['id', 'name', 'volume']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'weight', 'daily_target']

class WaterIngestedSerializer(serializers.ModelSerializer):
    volume = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = WaterIngested
        fields = ['id', 'user_name', 'volume', 'date']

    def get_volume(self, obj):
        return obj.amount_ml.volume

    def get_user_name(self, obj):
        return obj.user.name