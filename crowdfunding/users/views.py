from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import CustomUserSerializer
from projects.models import Project
from .token_serializers import TokenSerializer

# Custom Pagination for User Lists
class UserPagination(PageNumberPagination):
    page_size = 10

# List All Users
class CustomUserList(APIView):
  permission_classes = [AllowAny]

  def get(self, request):
      users = CustomUser.objects.all()
      
      serializer = CustomUserSerializer(users, many=True)
      return Response(serializer.data)

  def post(self, request):
      serializer = CustomUserSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(
              serializer.data,
              status=status.HTTP_201_CREATED
          )
      custom_errors = {
            field: " ".join(errors) for field, errors in serializer.errors.items()
        }
      return Response(
            {"detail": "Validation failed", "errors": custom_errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

# User Detail: GET, PUT, PATCH, DELETE
class CustomUserDetail(APIView):
   permission_classes = [IsAuthenticated]

   def get_object(self, pk):
       try:
           return CustomUser.objects.get(pk=pk)
       except CustomUser.DoesNotExist:
           raise Http404

   def get(self, request, pk):
       user = self.get_object(pk)
       serializer = CustomUserSerializer(user)
       return Response(serializer.data)
   
   def put(self, request, pk):
       user = self.get_object(pk)
       serializer = CustomUserSerializer(user, data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def patch(self, request, pk):
       user = self.get_object(pk)
       serializer = CustomUserSerializer(user, data=request.data, partial=True)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def delete(self, request, pk):
       user = self.get_object(pk)
       user.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)
   
   # Organisation Views (Previously in organisations/views.py)
class OrganisationList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        organisations = CustomUser.objects.filter(role="organisation")
        serializer = CustomUserSerializer(organisations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(role="organisation")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        custom_errors = {
            field: " ".join(errors) for field, errors in serializer.errors.items()
        }
        return Response(
            {"detail": "Validation failed", "errors": custom_errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

class OrganisationDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            organisation = CustomUser.objects.get(pk=pk, role="organisation")
            return organisation
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        organisation = self.get_object(pk)
        serializer = CustomUserSerializer(organisation)
        return Response(serializer.data)