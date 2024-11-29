from django.contrib.auth.models import AbstractUser
from django.db import models
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('organisation', 'Organisation'),
        ('user', 'User'),
    ]
    # role field for user type
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user', # Default to 'user' role
    )

    # Additional fields
    email = models.EmailField(unique=True, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)
    

   # Role checking
    def is_supporter(self):
        return self.role == 'user'
    
    def is_organisation(self):
        return self.role == 'organisation'
     
    def __str__(self):
       return f"{self.username} {self.role}"