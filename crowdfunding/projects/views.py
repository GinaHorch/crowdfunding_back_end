from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView # Required for class-based views like APIView
from rest_framework.response import Response # Required for sending responses
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView # Used for paginated ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from .models import Project, Pledge, Category
from .serializers import ProjectSerializer, PledgeSerializer, CategorySerializer, ProjectDetailSerializer, PledgeDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly

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
        # Ensure only organisations can create projects
        if not hasattr(request.user, "is_organisation") or not request.user.is_organisation():
            return Response(
                {"detail": "Only organisations can create projects."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Add organisation to the request data
        data = request.data.copy()
        data["organisation"] = request.user.id

        # Validate and save the project
        serializer = ProjectSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
  
class ProjectDetail(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [
       permissions.IsAuthenticatedOrReadOnly,
       IsOwnerOrReadOnly
   ]

    def update(self, request, *args, **kwargs):
        # Restrict updates to the organisation that created the project
        project = self.get_object()
        if request.user != project.organisation:
            return Response(
                {"detail": "You do not have permission to edit this project."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Restrict deletion to the organisation that created the project
        project = self.get_object()
        if request.user != project.organisation:
            return Response(
                {"detail": "You do not have permission to delete this project."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

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
       pledge.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)

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

def custom_404_view(request, exception=None):
   return Response({'error':'The resource was not found'}, status=status.HTTP_404_NOT_FOUND)

def custom_500_view(request):
   return Response({'error': 'An internal server error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)