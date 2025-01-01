from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView # Required for class-based views like APIView
from rest_framework.response import Response # Required for sending responses
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView # Used for paginated ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
import os
from .models import Project, Pledge, Category
from .serializers import ProjectSerializer, PledgeSerializer, CategorySerializer, ProjectDetailSerializer, PledgeDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly
from botocore.exceptions import ClientError
import boto3
from django.conf import settings

class ProjectPagination(PageNumberPagination):
   page_size = 10

class ProjectList(ListAPIView):
    queryset = Project.objects.all().order_by("title")
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = ProjectPagination 

class ProjectCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    def post(self, request):
        print("Request Headers:", request.headers)
        print("Authenticated User:", request.user) 
        print("Request Data:", request.data)
        print("Request Files:", request.FILES)

        # Ensure only organisations can create projects
        if not hasattr(request.user, "is_organisation") or not request.user.is_organisation():
            return Response(
                {"detail": "Only organisations can create projects."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Add organisation to the request data
        data = request.data.copy()
        data["organisation"] = request.user.id

        # Get the image from the request
        image = request.FILES.get('image')
        # If an image is provided, add it to the request data
        if image:
            print("Image detected:", image.name)
            try: 
                s3 = boto3.client(
                   's3',
                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                   region_name=settings.AWS_S3_REGION_NAME,
                )
                s3.upload_fileobj(
                    image,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    f"project_images/{image.name}"
                )
                print(f"Successfully uploaded {image.name} to S3.") 
                data["image"] = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/project_images/{image.name}"
            except ClientError as e:
                print(f"Failed to upload {image.name} to S3: {e}")
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            data["image"] = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/project_images/placeholder.webp"

        # Validate and save the project
        try:
            serializer = ProjectSerializer(data=data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            print("Validated Data", serializer.validated_data)
            serializer.save()
            print("Project created successfully:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Serializer Error:", str(e))  # Debug serializer errors
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class ProjectDetail(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'pk'
    permission_classes = [
       permissions.IsAuthenticatedOrReadOnly,
       IsOwnerOrReadOnly
   ]
    
    def get_object(self):
        obj = super().get_object()
        print("Fetched object in ProjectDetail:", obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        # Restrict updates to the organisation that created the project
        print("Update method called in ProjectDetail")
        project = self.get_object()
        if request.user != project.organisation:
            return Response(
                {"detail": "You do not have permission to edit this project."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Restrict deletion to the organisation that created the project
        print("Destroy method called in ProjectDetail")
        project = self.get_object()
        if request.user != project.organisation:
            return Response(
                {"detail": "You do not have permission to delete this project."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

class ProjectPledgeCreateView(APIView):
    def post(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        if not project.is_open:
            return Response(
                {"detail": "You cannot pledge to a closed project."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PledgeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pledge = serializer.save(supporter=request.user, project=project)  # Associate pledge with project
        project.current_amount += pledge.amount
        project.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PledgeList(APIView):
   permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   def get(self, request):
      pledges = Pledge.objects.all()
      serializer = PledgeSerializer(pledges, many=True)
      return Response(serializer.data)

   def post(self, request):
      serializer = PledgeSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)

    # Check if the project is open for pledges
      project = serializer.validated_data.get('project')
      if not project.is_open:
        return Response(
            {"detail": "You cannot pledge to a closed project."},
            status=status.HTTP_400_BAD_REQUEST
        )
      
      serializer.save(supporter=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

class PledgeDetail(APIView):
    permission_classes = [
       permissions.IsAuthenticatedOrReadOnly,
       IsSupporterOrReadOnly
   ]

    def get_object(self, pk):
       try:
           pledge = Pledge.objects.get(pk=pk)
           self.check_object_permissions(self.request, pledge)
           return pledge
       except Pledge.DoesNotExist:
           raise Http404({"detail": "Pledge not found."})

    def get(self, request, pk):
       pledge = self.get_object(pk)
       serializer = PledgeDetailSerializer(pledge)
       return Response(serializer.data)
   
    def put(self, request, pk):
       pledge = self.get_object(pk)
       serializer = PledgeDetailSerializer(
           instance=pledge,
           data=request.data,
           partial=True
       )
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data)
    
    def delete(self, request, pk):
       pledge = self.get_object(pk)
       if pledge.supporter == request.user:
            pledge.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
       else:
            return Response(
                {"detail": "You do not have permission to delete this pledge."},
                status=status.HTTP_403_FORBIDDEN
            )

class CategoryListCreate(APIView):
    def post(self, request):
       serializer = CategorySerializer(data=request.data)
       serializer.is_valid(raise_exception=True)

    # Check for duplicates
       if Category.objects.filter(name=serializer.validated_data['name']).exists():
          return Response(
             {"detail": "A category with this name already exists."},
             status=status.HTTP_400_BAD_REQUEST
          )

       serializer.save()
       return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
      categories = Category.objects.all()
      serializer = CategorySerializer(categories, many=True)
      return Response(serializer.data)

class ProjectUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def patch(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            print(f"Updating project: {project.title}")
        except Project.DoesNotExist:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the current user is the project owner
        if request.user != project.organisation:
            return Response(
                {"detail": "You do not have permission to edit this project."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        data = request.data.copy()
        
        # Handle image upload via S3
        image = request.FILES.get("image")
        if image:
            print(f"Image detected for update: {image.name}")
            try:
                s3 = boto3.client(
                    "s3",
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME,
                )
                # Upload image to S3
                s3.upload_fileobj(
                    image,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    f"uploads/{image.name}"
                )
                # Update the image URL in the request data
                data["image"] = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/project_images/{image.name}"
                print(f"Image successfully uploaded to S3: {data['image']}")
            except ClientError as e:
                print(f"Error uploading image to S3: {e}")
                return Response(
                    {"detail": "Failed to upload image to S3."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # Validate and update the project using the serializer
        serializer = ProjectSerializer(project, data=data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            print(f"Project updated successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request):
        print("Request Files:", request.FILES)
        media_dir = settings.MEDIA_ROOT
        if not os.access(media_dir, os.W_OK):
            print(f"Media directory '{media_dir}' is not writable")
        else:
            print(f"Media directory '{media_dir}' is writable")
    
        
def custom_404_view(request, exception=None):
   return Response({'error':'The resource was not found'}, status=status.HTTP_404_NOT_FOUND)

def custom_500_view(request):
   return Response({'error': 'An internal server error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)