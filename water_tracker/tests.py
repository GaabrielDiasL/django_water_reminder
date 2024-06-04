# water_tracker/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, CupSize, WaterIngested

class WaterIngestedAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name='Alice', weight=70)
        self.cup_size_small = CupSize.objects.create(name='Copo pequeno', volume=250)
        self.cup_size_medium = CupSize.objects.create(name='Copo médio', volume=350)
        self.cup_size_large = CupSize.objects.create(name='Garrafa média', volume=500)
        self.water_ingested_url = reverse('wateringested-list')
        self.daily_status_url = lambda user_id: reverse('wateringested-daily-status', kwargs={'user_id': user_id})
        self.history_url = lambda user_id: reverse('wateringested-history', kwargs={'user_id': user_id})

    def test_create_water_ingested(self):
        data = {
            'user': self.user.id,
            'amount_ml': self.cup_size_small.id,
            'date': '2024-06-03'
        }
        response = self.client.post(self.water_ingested_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['amount_ml'], self.cup_size_small.id)
        self.assertEqual(response.data['volume'], 250)

    def test_get_daily_status(self):
        WaterIngested.objects.create(user=self.user, amount_ml=self.cup_size_small, date='2024-06-04')
        response = self.client.get(self.daily_status_url(self.user.id), {'date': '2024-06-04'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_ingested'], 250)
        self.assertEqual(response.data['remaining'], 2450 - 250)
        self.assertEqual(response.data['daily_target_met'], False)
        self.assertEqual(response.data['percentage_consumed'], round((250 / 2450) * 100, 2))

    def test_get_history(self):
        WaterIngested.objects.create(user=self.user, amount_ml=self.cup_size_small, date='2024-06-03')
        WaterIngested.objects.create(user=self.user, amount_ml=self.cup_size_medium, date='2024-06-04')
        response = self.client.get(self.history_url(self.user.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['amount_ml'], self.cup_size_small.id)
        self.assertEqual(response.data[0]['volume'], 250)
        self.assertEqual(response.data[1]['amount_ml'], self.cup_size_medium.id)
        self.assertEqual(response.data[1]['volume'], 350)
