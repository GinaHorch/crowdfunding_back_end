from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
import boto3

class Category(models.Model):
   name = models.CharField(max_length=100)
   
   def __str__(self):
      return self.name
   
class Project(models.Model):
   title = models.CharField(max_length=200)
   description = models.TextField()
   target_amount = models.IntegerField()
   current_amount = models.IntegerField(default=0)
   image = models.ImageField(upload_to="project_images/", blank=True, null=True, max_length=500)
   location = models.TextField()
   is_open = models.BooleanField(default=True)
   date_created = models.DateTimeField(auto_now_add=True)
   end_date = models.DateTimeField(null=True)
   
   category = models.ForeignKey(
      Category,
      on_delete=models.SET_NULL,
      null=True,
      related_name='projects'
   ) 
   organisation = models.ForeignKey(
      'users.CustomUser',
      on_delete=models.CASCADE,
      related_name='projects'
   )

   def __str__(self):
      return self.title
   
   def clean(self):
      if self.target_amount < 0:
         raise ValidationError("Target amount cannot be negative.")
      if self.current_amount < 0:
         raise ValidationError("Current amount cannot be negative.")
      if self.current_amount > self.target_amount:
         raise ValidationError("Current amount cannot exceed target amount.")
   
   def save(self, *args, **kwargs):
      print(f"Image field before save: {self.image}")
      self.clean()
      if self.image and not str(self.image).startswith("http"):
        # Upload image to S3 if it's a local file
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        try:
            s3.upload_fileobj(
                self.image.file,  # Upload the file-like object
                settings.AWS_STORAGE_BUCKET_NAME,
                f"project_images/{self.image.name}"
            )
            # Replace the image field with the S3 URL
            self.image = f"project_images/{self.image.name}"
        except Exception as e:
            raise ValueError(f"Error uploading image to S3: {e}")
      super().save(*args, **kwargs)
    
class Pledge(models.Model):
   amount = models.PositiveIntegerField()
   comment = models.CharField(max_length=200, blank=True)
   anonymous = models.BooleanField(default=False)
   pledge_date = models.DateTimeField(auto_now_add=True)
   project = models.ForeignKey(
       'Project',
       on_delete=models.CASCADE,
       related_name='pledges'
   )
   supporter = models.ForeignKey(
       'users.CustomUser',
       on_delete=models.CASCADE,
       related_name='pledges'
   )

   def __str__(self):
      return f"{self.supporter.username} - {self.amount} for {self.project.title}"
   
   def clean(self):
      if not self.project:
          raise ValidationError("Pledge must be associated with a project.")
      if self.amount > (self.project.target_amount - self.project.current_amount):
        raise ValidationError("Pledge exceeds the funding target.")