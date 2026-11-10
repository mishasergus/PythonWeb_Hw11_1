from django.db import models

# Create your models here.
class Parcel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    tracking_number = models.CharField(max_length=15, unique=True)