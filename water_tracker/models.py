from django.db import models

class CupSize(models.Model):
    name = models.CharField(max_length=100)
    amount_ml = models.FloatField()

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def daily_target(self):
        return self.weight * 35

class WaterIngested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_ml = models.ForeignKey(CupSize, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)