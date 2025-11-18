from rest_framework import serializers
from models import Vehicle, VehicleImages

class VehicleImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImages
        fields = ['id', 'image']


class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = '__all__'