from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from users.models import CustomUser
from organisations.models import OrganisationProfile

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid username or password")

        # Determine role based on associated OrganisationProfile
        if hasattr(user, 'organisationprofile'):
            role = 'organisation'
        else:
            role = 'user'

        # Add role to the serializer context
        self.context['role'] = role
        self.context['user'] = user
        return data

    def create(self, validated_data):
        # Return user and role context
        return {
            "user": self.context['user'],
            "role": self.context['role']
        }