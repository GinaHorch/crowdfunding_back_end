from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):

    USER_TYPES = (
        (1, 'Supporter'),
        (2, 'Organisation'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default=1)

    # Shared fields
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)

    # Fields specific to 'Supporter'
    pledge_id = models.ForeignKey(
        'projects.Pledge',
        on_delete=models.CASCADE,
        related_name='supporter_pledges',
        null=True, blank=True
    )

    # Fields specific to 'Organisation'
    organisation_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    project_id = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='organisation_projects',
        null=True, blank=True
    )

    # Define a method to check user type
    def is_supporter(self):
        return self.user_type == 'supporter'
    
    def is_organisation(self):
        return self.user_type == 'organisation'
    
    def __str__(self):
       return self.username