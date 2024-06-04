from django.shortcuts import render
from rest_framework import viewsets
from .models import User, WaterIngested
from .serializers import UserSerializer, WaterIngestedSerializer
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Sum
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class WaterIngestedViewSet(viewsets.ModelViewSet):
    queryset = WaterIngested.objects.all()
    serializer_class = WaterIngestedSerializer

    @action(detail=False, methods=['get'], url_path='daily-status/(?P<user_id>[^/.]+)')
    def daily_status(self, request, user_id=None):
        today = timezone.now().date()
        user = User.objects.get(id=user_id)
        total_ingested = WaterIngested.objects.filter(user=user, date=today).aggregate(Sum('amount_ml'))['amount_ml__sum'] or 0
        remaining = user.daily_target - total_ingested
        return Response(
            {
                'total_ingested': total_ingested,
                'remaining': remaining,
                'daily_target': user.daily_target,
            }
        )
    
    @action(detail=False, methods=['get'], url_path='history/(?P<user_id>[^/.]+)')
    def history(self, request, user_id=None):
        user = User.objects.get(id=user_id)
        history = WaterIngested.objects.filter(user=user)
        serializer = WaterIngestedSerializer(history, many=True)
        return Response(serializer.data)