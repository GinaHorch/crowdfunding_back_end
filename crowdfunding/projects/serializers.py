from rest_framework import serializers
from django.apps import apps
from .models import Project, Pledge, Category
from users.models import CustomUser
from django.db.models import Sum

class PledgeSerializer(serializers.ModelSerializer):
  supporter_id = serializers.ReadOnlyField(source='supporter.id')
  supporter_name = serializers.ReadOnlyField(source='supporter.username')
  project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())  # Ensure project exists
  class Meta:
      model = Pledge
      fields = ['id', 'supporter_id', 'supporter_name', 'project', 'amount', 'comment', 'anonymous', 'pledge_date']
  def validate_amount(self, value):
     if value <= 0:
        raise serializers.ValidationError("Pledge amount must be greater than zero.")
     return value

class ProjectSerializer(serializers.ModelSerializer):
   organisation = serializers.ReadOnlyField(source='organisation.id')
   image = serializers.ImageField(allow_null=True, required=False)
   class Meta:
      model = Project
      fields = [
         'id', 
         'title', 
         'description', 
         'target_amount', 
         'current_amount', 
         'organisation', 
         'image',
         'date_created', 
         'location',
         'is_open', 
         'end_date', 
         'category', 
         'pledges' 
      ]
   pledges = serializers.SerializerMethodField()   # dynamically include pledges
   current_amount = serializers.SerializerMethodField()  # dynamically include current amount

   def get_pledges(self, obj):
      """Return all pledges for the project."""
      pledges = obj.pledges.all()
      return PledgeSerializer(pledges, many=True).data
   
   def get_current_amount(self, obj):
      """Calculate total pledged amount."""
      total = obj.pledges.aggregate(total=Sum('amount'))['total']
      return total or 0  # Default to 0 if there are no pledges
   
   def create(self, validated_data):
        print("Context:", self.context)
        print("Validated Data:", validated_data)
        # Retrieve the user from the serializer's context
        if "image" not in validated_data or validated_data["image"] is None:
            validated_data["image"] = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/project_images/placeholder.webp"

        # Retrieve the user from the serializer's context
        user = self.context["request"].user    
        
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