from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from organisations.permissions import IsOrganisationStaff  # Custom permission for staff
from .models import Project
from .serializers import ProjectSerializer

class ProjectCreationViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOrganisationStaff]