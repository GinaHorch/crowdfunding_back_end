from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Project(models.Model):
   title = models.CharField(max_length=200)
   description = models.TextField()
   target_amount = models.IntegerField()
   current_amount = models.IntegerField()
   image_url = models.URLField()
   location = models.TextField()
   is_open = models.BooleanField()
   date_created = models.DateTimeField(auto_now_add=True)
   end_date = models.DateTimeField()
   user_id = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='organisation_projects'
   )
   category = models.ForeignKey(
      get_user_model(),
      on_delete=models.CASCADE,
      related_name='project_category'
   ) 
   organisation = models.ForeignKey(
      'users.CustomUser',
      on_delete=models.CASCADE,
      related_name='projects'
   )

   def __str__(self):
      return self.title
    
class Pledge(models.Model):
   amount = models.IntegerField()
   comment = models.CharField(max_length=200)
   anonymous = models.BooleanField()
   pledge_date = models.DateTimeField(auto_now_add=True)
   project = models.ForeignKey(
       'Project',
       on_delete=models.CASCADE,
       related_name='project_pledges'
   )
   supporter = models.ForeignKey(
       get_user_model(),
       on_delete=models.CASCADE,
       related_name='supporter_pledges'
   )