from rest_framework import serializers


class CreatePaymentSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
