from django.contrib.auth import get_user_model
from django.db import models
from vehicles.models import Vehicle
from django_jalali.db import models as jmodels
from decimal import Decimal

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_total(self):
        return sum((item.total_price or 0) for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.phone_number}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE)
    start_time = jmodels.jDateTimeField()
    end_time = jmodels.jDateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_item(self):

        duration = self.end_time - self.start_time
        hours = Decimal(duration.total_seconds()) / Decimal(3600)
        days = hours // 24


        if days >= 1:
            hours = hours - (days * 24)
            print(hours)
            print(days)
            return (days * self.vehicle.price_per_day) + (hours * self.vehicle.price_per_hour)

        return hours * self.vehicle.price_per_hour

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_item
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle.name} — {self.start_time} to {self.end_time}"
