from django.contrib import admin

from reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'start_time', 'end_time', 'total_price', 'status', 'created_at')
