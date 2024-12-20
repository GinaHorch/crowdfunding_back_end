from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class Category(models.Model):
   name = models.CharField(max_length=100)
   
   def __str__(self):
      return self.name
   
class Project(models.Model):
   title = models.CharField(max_length=200)
   description = models.TextField()
   target_amount = models.IntegerField()
   current_amount = models.IntegerField(default=0)
   # image_url = models.URLField(null=True, blank=True)
   image = models.ImageField(upload_to="", blank=True, null=True)
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
      self.clean()
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