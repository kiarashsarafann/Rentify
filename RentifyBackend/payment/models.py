from django.db import models
from django.contrib.auth import get_user_model
from reservation.models import Reservation

User = get_user_model()

class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    authority = models.CharField(max_length=255, blank=True, null=True)
    ref_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
