from rest_framework import serializers
from django.apps import apps
from .models import Project, Pledge, Category
from users.models import CustomUser

class PledgeSerializer(serializers.ModelSerializer):
  supporter = serializers.ReadOnlyField(source='supporter.id')
  project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())  # Ensure project exists
  class Meta:
      model = Pledge
      fields = ['id', 'supporter', 'project', 'amount', 'comment', 'anonymous', 'pledge_date']
  def validate_amount(self, value):
     if value <= 0:
        raise serializers.ValidationError("Pledge amount must be greater than zero.")
     return value

class ProjectSerializer(serializers.ModelSerializer):
    organisation = serializers.ReadOnlyField(source='organisation.id')
    image = serializers.ImageField(allow_null=True)
    class Meta:
      model = Project
      fields = ['id', 'title', 'description', 'target_amount', 
                'current_amount', 'organisation', 'image',
                'date_created', 'location',
                'is_open', 'end_date', 'category']

    def create(self, validated_data):
        print("Context:", self.context)
        print("Validated Data:", validated_data)
        # Retrieve the user from the serializer's context
        user = self.context['request'].user
        
        # Ensure the user has the organisation role
        if not user.is_authenticated or not user.is_organisation():
            raise serializers.ValidationError("Only organisations can create projects.")
        
        # Add the organisation to the validated data
        validated_data['organisation'] = user
        
        # Use the model's create method to create the object
        return super().create(validated_data)
            
class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = '__all__'
class ProjectDetailSerializer(ProjectSerializer):
  pledges = PledgeSerializer(many=True, read_only=True)
  class Meta:
     model = Project
     fields = ProjectSerializer.Meta.fields + ['pledges']

  def update(self, instance, validated_data):
     # Prevent organisation change
     validated_data.pop('organisation', None)
     return super().update(instance, validated_data)

class PledgeDetailSerializer(PledgeSerializer):
    def update(self, instance, validated_data):
     instance.supporter = validated_data.get('supporter', instance.supporter)
     instance.amount = validated_data.get('amount', instance.amount)
     instance.comment = validated_data.get('comment', instance.comment)
     instance.anonymous = validated_data.get('anonymous', instance.anonymous)
     instance.project = validated_data.get('project', instance.project)
     instance.save()
     return instance