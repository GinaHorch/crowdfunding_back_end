from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    ROLE_USER = 'user'
    ROLE_ORGANISATION = 'organisation'
    ROLE_CHOICES = [
        (ROLE_USER, 'User'),    
        (ROLE_ORGANISATION, 'Organisation'),
        
    ]
    # role field
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
    )
    # common user fields
    email = models.EmailField(unique=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="project_images/", blank=True, null=True)

    # Fields specific to 'Organisation'
    organisation_name = models.CharField(max_length=255, null=True, blank=True)
    organisation_contact = models.CharField(max_length=255, null=True, blank=True)
    organisation_phone_number = models.CharField(max_length=15, null=True, blank=True)
    organisation_ABN = models.CharField(max_length=11, unique=True, null=True, blank=True)
    is_charity = models.BooleanField(default=False)

    # Validations
    def clean(self):
        self.email = self.email.lower()
        # Validate ABN only for organisation roles
        if self.role == self.ROLE_ORGANISATION:
            if not self.organisation_ABN or not self.organisation_ABN.isdigit() or len(self.organisation_ABN) != 11:
                raise ValidationError("ABN must be exactly 11 numeric digits for organisations.")
        elif self.role == self.ROLE_USER:
            # Ensure organisation fields are empty for users
            if any([
                self.organisation_name,
                self.organisation_contact,
                self.organisation_phone_number,
                self.organisation_ABN,
            ]):
                raise ValidationError("Organisation fields must be empty for non-organisation users.")
        super().clean()
        
    def has_role(self, role):
        return self.is_active and self.role == role
    
    def is_supporter(self):
        return self.has_role(self.ROLE_USER)

    def is_organisation(self):
        return self.has_role(self.ROLE_ORGANISATION)

    def __str__(self):
        return f"{self.username} ({self.role}) - {self.email}"