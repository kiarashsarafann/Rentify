from rest_framework import serializers
from .models import Cart, CartItem
from vehicles.models import Vehicle


class CartItemSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source="vehicle.name", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "vehicle",
            "vehicle_name",
            "start_time",
            "end_time",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.total_price


