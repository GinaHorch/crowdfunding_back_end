from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer
from .token_serializers import TokenSerializer

class UserManagementViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing all users (both 'user' and 'organisation' roles).
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class OrganisationManagementViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing organisations.
    """
    queryset = CustomUser.objects.filter(role='organisation')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

# Unified Token Authentication View
class TokenAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context['user']
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
            }

            # Include organisation-specific details if applicable
            if user.role == "organisation":
                response_data["user"]["organisation_details"] = {
                    "organisation_name": user.organisation_name,
                    "organisation_contact": user.organisation_contact,
                    "organisation_ABN": user.organisation_ABN,
                    "is_charity": user.is_charity,
                }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
