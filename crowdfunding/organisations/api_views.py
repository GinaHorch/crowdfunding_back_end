from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import OrganisationProfile
from .serializers import OrganisationProfileSerializer

class OrganisationManagementViewSet(viewsets.ModelViewSet):
    queryset = OrganisationProfile.objects.all()
    serializer_class = OrganisationProfileSerializer
    permission_classes = [IsAuthenticated]