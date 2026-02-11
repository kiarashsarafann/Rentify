from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'reservation', 'amount', 'authority', 'ref_id', 'status', 'created_at')
