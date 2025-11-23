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


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    calculate_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "calculate_total"]
        read_only_fields = ["user", "items", "calculate_total"]

        def get_calculate_total(self, obj):
            return obj.calculate_total
