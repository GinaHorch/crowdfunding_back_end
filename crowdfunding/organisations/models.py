from django.db import models
from users.models import CustomUser
from django.conf import settings
from django.core.exceptions import ValidationError

class OrganisationProfile(models.Model):
    # One-to-one relationship with CustomUser
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name='organisation_profile'
    )

    # Fields specific to 'Organisation'
    organisation_name = models.CharField(max_length=255)
    organisation_contact = models.CharField(max_length=255)
    organisation_phone_number = models.CharField(max_length=15)
    organisation_email = models.EmailField(unique=True)
    organisation_image_url = models.URLField(null=True, blank=True)
    organisation_ABN = models.CharField(max_length=11, unique=True)
    is_charity = models.BooleanField(default=False)

    def __str__(self):
        return self.organisation_name
    
    def clean(self):
        if not self.organisation_ABN.isdigit() or len(self.organisation_ABN) != 11:
            raise ValidationError("ABN must be exactly 11 numeric digits")