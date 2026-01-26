from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
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
                    national_code=validated_data['national_code'], )
        user.set_password(validated_data['password'])
        user.username = validated_data['phone_number']
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(phone_number=data['phone_number'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Phone number does not exist")

        if not user.check_password(data['password']):
            raise serializers.ValidationError("Incorrect password")

        data['user'] = user
        return data
