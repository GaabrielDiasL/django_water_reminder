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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = WaterIngested
        fields = ['id', 'user', 'user_details', 'amount_ml', 'volume', 'date']

    def get_volume(self, obj):
        return obj.amount_ml.volume