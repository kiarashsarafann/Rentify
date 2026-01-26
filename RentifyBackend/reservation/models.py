from decimal import Decimal

from django.db import models
from django_jalali.db import models as jmodels

from django.contrib.auth import get_user_model

User = get_user_model()


class ReservationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELED = "canceled", "Canceled"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE)
    start_time = jmodels.jDateTimeField()
    end_time = jmodels.jDateTimeField()

    status = models.CharField(
        max_length=10,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def calculate_price(self):
        duration = self.end_time - self.start_time
        hours = Decimal(duration.total_seconds()) / Decimal(3600)
        days = hours // 24

        if days >= 1:
            hours = hours - (days * 24)
            return (days * self.vehicle.price_per_day) + (hours * self.vehicle.price_per_hour)

        return hours * self.vehicle.price_per_hour

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_price
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} | {self.total_price} | {self.status}"
