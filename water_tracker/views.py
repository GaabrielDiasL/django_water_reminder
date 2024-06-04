from django.shortcuts import render
from rest_framework import viewsets
from .models import User, WaterIngested, CupSize
from .serializers import UserSerializer, WaterIngestedSerializer, CupSizeSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Sum
from rest_framework.response import Response
import datetime

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CupSizeViewSet(viewsets.ModelViewSet):
    queryset = CupSize.objects.all()
    serializer_class = CupSizeSerializer

class WaterIngestedViewSet(viewsets.ModelViewSet):
    queryset = WaterIngested.objects.all()
    serializer_class = WaterIngestedSerializer

    @action(detail=False, methods=['get'], url_path='daily-status/(?P<user_id>[^/.]+)')
    def daily_status(self, request, user_id=None):
        date_str = request.query_params.get('date')
        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Date format should be YYYY-MM-DD")
        else:
            date = timezone.now().date()

        user = User.objects.get(id=user_id)
        total_ingested = WaterIngested.objects.filter(user=user, date=date).aggregate(total_volume=Sum('amount_ml__volume'))['total_volume'] or 0
        remaining = user.daily_target - total_ingested
        percentage_consumed = round((total_ingested / user.daily_target) * 100, 2) if user.daily_target > 0 else 0

        return Response(
            {
                'total_ingested': total_ingested,
                'remaining': remaining,
                'daily_target_met': total_ingested >= user.daily_target,
                'daily_target': user.daily_target,
                'date': date,
                'percentage_consumed': percentage_consumed,
            }
        )
    
    @action(detail=False, methods=['get'], url_path='history/(?P<user_id>[^/.]+)')
    def history(self, request, user_id=None):
        user = User.objects.get(id=user_id)
        history = WaterIngested.objects.filter(user=user)
        serializer = WaterIngestedSerializer(history, many=True)
        return Response(serializer.data)