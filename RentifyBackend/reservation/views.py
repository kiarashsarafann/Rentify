from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Reservation, ReservationStatus
from .serializers import ReservationSerializer

class ReservationViewSet(
    mixins.ListModelMixin,      # GET list
    mixins.RetrieveModelMixin,  # GET detail
    mixins.CreateModelMixin,    # POST
    mixins.UpdateModelMixin,    # PATCH/PUT
    viewsets.GenericViewSet
):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

