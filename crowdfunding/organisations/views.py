from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from users.models import CustomUser
from .models import OrganisationProfile
from users.serializers import CustomUserSerializer
from .serializers import OrganisationProfileSerializer
from projects.models import Project
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
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
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
   
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        organisation = serializer.validated_data['organisation']
        token, created = Token.objects.get_or_create(organisation=organisation)

        return Response({
            'token': token.key,
            'organisation_id': organisation.id,
            'email': organisation.email
        })