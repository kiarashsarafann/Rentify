from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'phone_number',
            'first_name',
            'last_name',
            'national_code',
            'password',
        ]

        def create(self, validated_data):
            user = User(phone_number=validated_data['phone_number'],
                        first_name=validated_data['first_name'],
                        last_name=validated_data['last_name'],
                        national_code=validated_data['national_code'],)
            user.set_password(validated_data['password'])
            user.save()
            return user