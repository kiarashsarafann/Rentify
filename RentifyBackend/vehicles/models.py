from django.db import models


# types for Vehicle.type
class VehicleType(models.TextChoices):
    CAR = 'car', 'Car'
    MOTORCYCLE = 'motorcycle', 'Motorcycle'


class Vehicle(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=10, choices=VehicleType.choices, default=VehicleType.CAR)
    brand = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    year = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=32)
    price_per_hour = models.DecimalField(max_digits=8,decimal_places=0, null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

#Images for Vehicles
class VehicleImages(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicle_images/')
