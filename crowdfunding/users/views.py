from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import CustomUserSerializer
from projects.models import Project
from .token_serializers import TokenSerializer

class CustomUserList(APIView):
  permission_classes = [permissions.AllowAny]
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
      return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
       )

class CustomUserDetail(APIView):
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

# New Unified Token Authentication View
class TokenAuthView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access the token endpoint

    def post(self, request, *args, **kwargs):
        # Use the unified TokenSerializer
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context['user']
            role = serializer.context['role']
            token, created = Token.objects.get_or_create(user=user)

            # Generate or retrieve the token for the authenticated user
            
            response_data = {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": role
                }
            }
            if role == "organisation":
                organisation = getattr(user, 'organisation_profile', None)
                if organisation:
                    response_data["user"]["organisation_name"] = organisation.organisation_name

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)