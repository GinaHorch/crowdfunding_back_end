from rest_framework import serializers
from django.apps import apps
from users.models import CustomUser
from .models import OrganisationProfile
 
class OrganisationProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model = apps.get_model('organisations.OrganisationProfile')
       fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    organisation_profile = OrganisationProfileSerializer()

    class Meta:
        model = CustomUser
        fields = '__all__'