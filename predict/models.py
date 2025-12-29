from django.db import models

class HousePricePrediction(models.Model):
    Income = models.FloatField()
    Age = models.FloatField()
    Room = models.FloatField()
    Bedroom = models.FloatField()
    Population = models.FloatField()
    Price = models.CharField(max_length=30)

    def __str__(self):
        return self.Price

