from django.db import models
from users.models import CustomUser
from django.conf import settings

# Create your models here.
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
    project_id = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='organisation_projects',
        null=True, blank=True
    )
    organisation_image_url = models.URLField(null=True, blank=True)
    organisation_ABN = models.CharField(max_length=11, unique=True)
    is_charity = models.BooleanField()

    # Owners and Staff
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='owned_organisations'
    )

    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='staff_organisations'
    )

    def __str__(self):
        return self.organisation_name