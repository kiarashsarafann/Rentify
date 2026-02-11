from django.db import models


# types for Vehicle.type
class VehicleType(models.TextChoices):
    CAR = 'car', 'Car'
    MOTORCYCLE = 'motorcycle', 'Motorcycle'


class Vehicle(models.Model):
    name = models.CharField(max_length=64, verbose_name='نام')
    type = models.CharField(max_length=10, choices=VehicleType.choices, default=VehicleType.CAR, verbose_name='نوع')
    brand = models.CharField(max_length=32, verbose_name='برند')
    model = models.CharField(max_length=32, verbose_name='مدل')
    year = models.IntegerField(null=True, blank=True, verbose_name='سال تولید')
    color = models.CharField(max_length=32, verbose_name='رنگ')
    price_per_hour = models.DecimalField(max_digits=8,decimal_places=0, null=True, blank=True, verbose_name='قیمت در ساعت')
    price_per_day = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True, verbose_name='قیمت در روز')
    is_available = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'وسیله نقلیه'
        verbose_name_plural = 'وسایل نقلیه'

    def __str__(self):
        return self.name

#Images for Vehicles
class VehicleImages(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images', verbose_name='وسیله')
    image = models.ImageField(upload_to='vehicle_images/', verbose_name='عکس')

    class Meta:
        db_table = 'vehicles_vehicle_images'
        verbose_name = 'عکس وسیله نقلیه'
        verbose_name_plural = 'عکس های وسایل نقلیه'

    def __str__(self):
        image_number = 0
        return self.vehicle.name + " | " + str(self.image)