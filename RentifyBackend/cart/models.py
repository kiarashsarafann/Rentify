from django.db import models

from users.models import User
from vehicles.models import Vehicle


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle")

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    total_price = models.DecimalField(max_digits=10, decimal_places=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_price(self):
        duration = self.end_datetime - self.start_datetime
        hours = duration.total_seconds() / 3600

        if hours >= 24:
            days = hours // 24
            return days * self.vehicle.price_per_day

        return hours * self.vehicle.price_per_hour

