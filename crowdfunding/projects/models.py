from django.db import models
from django.contrib.auth import get_user_model
from organisations.models import OrganisationProfile

# Create your models here.
class Category(models.Model):
   name = models.CharField(max_length=100)
   description = models.TextField()
   image_url = models.URLField(null=True, blank=True)

   def __str__(self):
      return self.name
class Project(models.Model):
   title = models.CharField(max_length=200)
   description = models.TextField()
   target_amount = models.IntegerField()
   current_amount = models.IntegerField(default=0)
   image_url = models.URLField(null=True, blank=True)
   location = models.TextField()
   is_open = models.BooleanField(default=True)
   date_created = models.DateTimeField(auto_now_add=True)
   end_date = models.DateTimeField()
   
   user_id = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='organisation_projects'
   )
   category = models.ForeignKey(
      Category,
      on_delete=models.SET_NULL,
      null=True,
      related_name='projects'
   ) 
   organisation = models.ForeignKey(
      OrganisationProfile,
      on_delete=models.CASCADE,
      related_name='projects'
   )

   def __str__(self):
      return self.title
    
class Pledge(models.Model):
   amount = models.IntegerField()
   comment = models.CharField(max_length=200, blank=True)
   anonymous = models.BooleanField(default=False)
   pledge_date = models.DateTimeField(auto_now_add=True)
   project = models.ForeignKey(
       'Project',
       on_delete=models.CASCADE,
       related_name='pledges'
   )
   supporter = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='pledges'
   )

   def __str__(self):
      return f"{self.supporter.username} - {self.amount} for {self.project.title}"