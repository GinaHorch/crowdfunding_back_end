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
from django.contrib.auth.models import User

# Custom Pagination for User Lists
class UserPagination(PageNumberPagination):
    page_size = 10

# List All Users
class CustomUserList(APIView):
  permission_classes = [permissions.AllowAny]

  def get(self, request):
      users = CustomUser.objects.all()
      
      serializer = CustomUserSerializer(users, many=True)
      return Response(serializer.data)

  def post(self, request):
      print("Raw request data:", request.data)  # Log raw incoming data
      serializer = CustomUserSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(
              serializer.data,
              status=status.HTTP_201_CREATED
          )
       
      print("Serializer Errors:", serializer.errors)
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

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]  # Signup is open to everyone

    def post(self, request):
        # Extract user data
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")  # 'user' or 'organisation'

        # Validate common fields
        if not username or not password or not role:
            return Response(
                {"detail": "Username, password, email, and role are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure email is unique
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"detail": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure username is unique
        if CustomUser.objects.filter(username=username).exists():
            return Response(
                {"detail": "A user with this username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Handle organisation-specific validations
        if role == CustomUser.ROLE_ORGANISATION:
            organisation_name = request.data.get("organisation_name")
            organisation_contact = request.data.get("organisation_contact")
            organisation_phone_number = request.data.get("organisation_phone_number")
            organisation_ABN = request.data.get("organisation_ABN")
            is_charity = request.data.get("is_charity", False)

            # Validate organisation fields
            if not organisation_name or not organisation_ABN:
                return Response(
                    {"detail": "Organisation name and ABN are required for organisations."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not organisation_ABN.isdigit() or len(organisation_ABN) != 11:
                return Response(
                    {"detail": "ABN must be exactly 11 numeric digits."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create organisation user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                organisation_name=organisation_name,
                organisation_contact=organisation_contact,
                organisation_phone_number=organisation_phone_number,
                organisation_ABN=organisation_ABN,
                is_charity=is_charity,
            )

        elif role == CustomUser.ROLE_USER:
            # Ensure organisation-specific fields are not provided for users
            organisation_fields = [
                "organisation_name",
                "organisation_contact",
                "organisation_phone_number",
                "organisation_ABN",
            ]
            for field in organisation_fields:
                if request.data.get(field):
                    return Response(
                        {"detail": f"{field} must be empty for users."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Create regular user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
            )

        else:
            return Response(
                {"detail": "Invalid role. Must be 'user' or 'organisation'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save and return success response
        user.save()
        return Response(
            {"message": "User created successfully!", "username": user.username, "role": user.role},
            status=status.HTTP_201_CREATED,
        )
