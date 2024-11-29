from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from users.models import CustomUser
from .models import OrganisationProfile
from users.serializers import CustomUserSerializer
from .serializers import OrganisationProfileSerializer
# Create your views here.

class OrganisationProfileList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        organisations = OrganisationProfile.objects.all()

        serializer = OrganisationProfileSerializer(organisations, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrganisationProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        custom_errors = {}
        for field, errors in serializer.errors.items():
            custom_errors[field] = " ".join(errors) # combine multiple errors
        
        return Response(
            {"detail": "Validation failed", "errors": custom_errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class OrganisationProfileDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
       try:
           organisation = OrganisationProfile.objects.get(pk=pk)
           self.check_object_permissions(self.request, organisation)
           return organisation
       except OrganisationProfile.DoesNotExist:
           raise Http404

    def get(self, request, pk):
       organisation = self.get_object(pk)
       serializer = OrganisationProfileSerializer(organisation)
       return Response(serializer.data)