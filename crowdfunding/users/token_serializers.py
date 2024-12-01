from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from users.models import CustomUser

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        print(f"Attempting to authenticate username: {username}")
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            print(f"Authentication failed for username: {username}")
            raise AuthenticationFailed("Invalid username or password.")
        if not user.is_active:
            raise AuthenticationFailed("This account is inactive.")
        if user.role == 'organisation':
            role = 'organisation'
        else:
            role = 'user'

        # Add role to the serializer context
        self.context['role'] = user.role
        self.context['user'] = user
        return data
    
    def create(self, validated_data):
        return {
            "user": self.context['user'],
            "role": self.context['role']
        }