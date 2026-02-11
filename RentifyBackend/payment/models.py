from django.db import models
from django.contrib.auth import get_user_model
from reservation.models import Reservation

User = get_user_model()

class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, verbose_name='رزرو')
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت کل')
    authority = models.CharField(max_length=255, blank=True, null=True, verbose_name='کد هویت')
    ref_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='کد رهگیری')
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'

    def __str__(self):
        return f"{self.user} | {self.ref_id}"
