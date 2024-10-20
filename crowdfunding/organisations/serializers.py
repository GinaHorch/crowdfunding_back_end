from rest_framework import serializers
from django.apps import apps
from users.models import CustomUser
from .models import OrganisationProfile
from projects.serializers import ProjectSerializer
 
class OrganisationProfileSerializer(serializers.ModelSerializer):
   projects = ProjectSerializer(many=True, read_only=True)  # Include projects
   class Meta:
       model = OrganisationProfile
       fields = ['id', 'organisation_name', 'organisation_contact', 'organisation_phone_number', 'organisation_ABN', 'is_charity', 'projects', 'user']

class CustomUserSerializer(serializers.ModelSerializer):
    organisation_profile = OrganisationProfileSerializer()

    class Meta:
        model = CustomUser
        fields = '__all__'

class OrganisationSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = OrganisationProfile
        fields = ['id', 'organisation_name', 'projects', 'organisation_contact', 'organisation_phone_number', 'organisation_ABN', 'is_charity']
        