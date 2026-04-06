from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError('This email already exists.')
        
        return data

    def create(self, data):
        user = User.objects.create_user(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        return user