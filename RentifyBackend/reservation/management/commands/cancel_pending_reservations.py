from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from reservation.models import Reservation, ReservationStatus


class Command(BaseCommand):
    help = "Cancel pending reservations older than 10 minutes"

    def handle(self, *args, **kwargs):
        limit_time = timezone.now() - timedelta(minutes=10)

        qs = Reservation.objects.filter(
            status=ReservationStatus.PENDING,
            created_at__lte=limit_time
        )

        updated = qs.update(status=ReservationStatus.CANCELED)

        self.stdout.write(f"{updated} reservations canceled.")
