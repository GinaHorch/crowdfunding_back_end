from rest_framework import serializers
from django.apps import apps
from .models import Project, Pledge, Category

class PledgeSerializer(serializers.ModelSerializer):
  supporter = serializers.ReadOnlyField(source='supporter.id')
  class Meta:
      model = Pledge
      fields = ['id', 'supporter', 'project', 'amount', 'comment', 'anonymous', 'pledge_date']
 
class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    class Meta:
      model = Project
      fields = ['id', 'title', 'description', 'target_amount', 'current_amount', 'owner', 'date_created', 'is_open', 'category']

class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = ['id', 'name']
class ProjectDetailSerializer(ProjectSerializer):
  pledges = PledgeSerializer(many=True, read_only=True)

  class Meta(ProjectSerializer):
     fields = ProjectSerializer.Meta.fields + ['pledges']

  def update(self, instance, validated_data):
     instance.title = validated_data.get('title', instance.title)
     instance.description = validated_data.get('description', instance.description)
     instance.target_amount = validated_data.get('target_amount', instance.goal)
     instance.image_url = validated_data.get('image_url', instance.image)
     instance.is_open = validated_data.get('is_open', instance.is_open)
     instance.date_created = validated_data.get('date_created', instance.date_created)
     instance.owner = validated_data.get('owner', instance.owner)
     instance.save()
     return instance

class PledgeDetailSerializer(PledgeSerializer):
    def update(self, instance, validated_data):
     instance.supporter = validated_data.get('supporter', instance.supporter)
     instance.amount = validated_data.get('amount', instance.amount)
     instance.comment = validated_data.get('comment', instance.comment)
     instance.anonymous = validated_data.get('anonymous', instance.anonymous)
     instance.project = validated_data.get('project', instance.project)
     instance.save()
     return instance