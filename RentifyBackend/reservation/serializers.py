from rest_framework import serializers
from django_jalali.serializers.serializerfield import JDateTimeField

from reservation.models import Reservation, ReservationStatus
from vehicles.models import Vehicle


class ReservationSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.IntegerField()
    vehicle_name = serializers.CharField(source="vehicle.name", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_name = serializers.CharField(source="user.name", read_only=True)
    start_time = JDateTimeField()
    end_time = JDateTimeField()
    status = serializers.CharField(source="status.name", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user_id",
            "user_name",
            "vehicle_id",
            "vehicle_name",
            "start_time",
            "end_time",
            "status",
            "total_price",
            "created_at",
        ]

    def get_total_price(self, obj):
        return obj.calculate_price

    def validate(self, data):
        if data["end_time"] <= data["start_time"]:
            raise serializers.ValidationError("زمان پایان باید بعد از شروع باشد")

        try:
            vehicle = Vehicle.objects.get(id=data["vehicle_id"])
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError("وسیله پیدا نشد")
        data["vehicle"] = vehicle

        if self.instance is None:
            if Reservation.objects.filter(vehicle=vehicle,
                                          status__in=[ReservationStatus.PENDING, ReservationStatus.CONFIRMED],
                                          start_time__lt=data["end_time"],
                                          end_time__gt=data["start_time"],
                                          ).exists():
                raise serializers.ValidationError("این بازه زمانی با یک آیتم دیگه تداخل دارد!")
        return data

    def update(self, instance, validated_data):
        instance.start_time = validated_data["start_time"]
        instance.end_time = validated_data["end_time"]
        instance.save()
        return instance
