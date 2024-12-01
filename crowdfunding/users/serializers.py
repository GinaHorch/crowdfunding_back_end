from rest_framework import serializers
from .models import CustomUser
from projects.models import Project

# Unified CustomUserSerializer
class CustomUserSerializer(serializers.ModelSerializer):
    # Nested organisation-specific fields
    organisation_details = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'date_joined', 'role',
            'organisation_details', 'date_created', 'image_url'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_organisation_details(self, obj):
        # Include organisation-specific details only for users with the organisation role
        if obj.role == CustomUser.ROLE_ORGANISATION:
            return {
                "organisation_name": obj.organisation_name,
                "organisation_contact": obj.organisation_contact,
                "organisation_phone_number": obj.organisation_phone_number,
                "organisation_ABN": obj.organisation_ABN,
                "is_charity": obj.is_charity,
            }
        return None
    
    def create(self, validated_data):
         # Use create_user to handle hashed password creation
        return CustomUser.objects.create_user(**validated_data)
    
# Serializer for Projects
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'target_amount', 'current_amount']