from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        logger.info(f"Attempting to authenticate username: {username}")
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            logger.warning("Authentication failed.")
            if CustomUser.objects.filter(username=username).exists():
                logger.warning(f"Incorrect password for username '{username}'.")
            else:
                logger.error(f"Username '{username}' does not exist.")
            raise AuthenticationFailed("Invalid username or password.")

        if not user.is_active:
            logger.warning(f"Account for username '{username}' is inactive.")
            raise AuthenticationFailed("This account is inactive.")

        # Add role to the serializer context
        self.context['role'] = user.role
        self.context['user'] = user
        return data
    
    def create(self, validated_data):
        return {
            "user": self.context['user'],
            "role": self.context['role']
        }