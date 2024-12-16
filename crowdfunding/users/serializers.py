from rest_framework import serializers
from .models import CustomUser
from projects.models import Project

# Unified CustomUserSerializer
class CustomUserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'date_joined', 'role',
            'organisation_name', 'organisation_contact', 'organisation_phone_number', 
            'organisation_ABN', 'is_charity', 'date_created', 'image',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """Validate payload based on role."""
        print("Validating data:", data)  # Debugging line

        role = data.get('role', CustomUser.ROLE_USER)

        if role == CustomUser.ROLE_ORGANISATION:
            # Validate that organisation-specific fields are present
            required_fields = [
                    'organisation_name', 
                    'organisation_contact', 
                    'organisation_phone_number', 
                    'organisation_ABN',
            ]
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({
                        field: f"{field} is required for organisation users."
                    })

            # Validate organisation_ABN
            organisation_ABN = data.get('organisation_ABN')
            if organisation_ABN and (not organisation_ABN.isdigit() or len(organisation_ABN) != 11):
                raise serializers.ValidationError({
                    "organisation_ABN": "ABN must be exactly 11 numeric digits."
                })

        elif role == CustomUser.ROLE_USER:
            # Ensure organisation-specific fields are not included
            organisation_fields = [
                'organisation_name', 
                'organisation_contact', 
                'organisation_phone_number', 
                'organisation_ABN',
            ]
            for field in organisation_fields:
                if data.get(field):
                    raise serializers.ValidationError({
                        field: f"{field} must not be provided for users with the role 'user'."
                    })
        print("Validated data:", data)        
        return data

    def create(self, validated_data):
        print("Creating user with validated data:", validated_data)
        """Create user with hashed password."""
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        print("User created successfully:", user)
        return user
    
# Serializer for Projects
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'target_amount', 'current_amount']

class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username", "email", "password", "confirm_password", "role",
            "organisation_name", "organisation_contact", "organisation_phone_number",
            "organisation_ABN", "is_charity"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """Perform role-specific and password validations."""
        # Password match validation
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})

        role = data.get("role", CustomUser.ROLE_USER)

        if role == CustomUser.ROLE_ORGANISATION:
            # Validate organisation-specific fields
            required_fields = [
                "organisation_name", "organisation_contact", 
                "organisation_phone_number", "organisation_ABN"
            ]
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f"{field} is required for organisations."})

            organisation_ABN = data.get("organisation_ABN")
            if organisation_ABN and (not organisation_ABN.isdigit() or len(organisation_ABN) != 11):
                raise serializers.ValidationError({"organisation_ABN": "ABN must be exactly 11 numeric digits."})

        elif role == CustomUser.ROLE_USER:
            # Ensure organisation-specific fields are not provided for users
            organisation_fields = [
                "organisation_name", "organisation_contact", 
                "organisation_phone_number", "organisation_ABN"
            ]
            for field in organisation_fields:
                if data.get(field):
                    raise serializers.ValidationError({field: f"{field} must be empty for regular users."})

        return data

    def create(self, validated_data):
        """Create the user with hashed password."""
        validated_data.pop("confirm_password")  # Remove confirm_password before saving
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user