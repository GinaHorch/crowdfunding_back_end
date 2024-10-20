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
    username = models.CharField(max_length=150, unique=True)

   # Define a method to check user type
    def is_supporter(self):
        return self.user_type == 1
    
    def is_organisation(self):
        return self.user_type == 2
     
    def __str__(self):
       return self.username