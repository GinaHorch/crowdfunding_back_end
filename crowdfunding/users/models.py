from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    ROLE_USER = 'user'
    ROLE_ORGANISATION = 'organisation'
    ROLE_CHOICES = [
        (ROLE_ORGANISATION, 'Organisation'),
        (ROLE_USER, 'User'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
    )
    email = models.EmailField(unique=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)

    def clean(self):
        self.email = self.email.lower()
        super().clean()
        
    def is_supporter(self):
        return self.is_active and self.role == self.ROLE_USER

    def is_organisation(self):
        return self.is_active and self.role == self.ROLE_ORGANISATION

    def __str__(self):
        return f"{self.username} ({self.role})"