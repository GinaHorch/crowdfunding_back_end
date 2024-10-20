from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import generics
from django.http import Http404
from .models import Project, Pledge, Category
from organisations.models import OrganisationProfile
from organisations.serializers import OrganisationSerializer
from .serializers import ProjectSerializer, PledgeSerializer, CategorySerializer, ProjectDetailSerializer, PledgeDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly
class ProjectList(APIView):
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]

  def get(self, request):
      projects = Project.objects.all()
      serializer = ProjectSerializer(projects, many=True)
      return Response(serializer.data)
  
  def post(self, request):
      if request.user.is_authenticated:
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save(owner=request.user)
          return Response(
              serializer.data,
              status=status.HTTP_201_CREATED
          )
      return Response(
          serializer.errors,
          status=status.HTTP_400_BAD_REQUEST
          )
  
class ProjectDetail(APIView):
   
   permission_classes = [
       permissions.IsAuthenticatedOrReadOnly,
       IsOwnerOrReadOnly
   ]

   def get_object(self, pk):
       try:
           project = Project.objects.get(pk=pk)
           self.check_object_permissions(self.request, project)
           return project
       except Project.DoesNotExist:
           raise Http404

   def get(self, request, pk):
       project = self.get_object(pk)
       serializer = ProjectDetailSerializer(project)
       return Response(serializer.data)
   
   def put(self, request, pk):
       project = self.get_object(pk)
       serializer = ProjectDetailSerializer(
           instance=project,
           data=request.data,
           partial=True
       )
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)

       return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST
       )

class PledgeList(APIView):
   permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   def get(self, request):
      pledges = Pledge.objects.all()
      serializer = PledgeSerializer(pledges, many=True)
      return Response(serializer.data)

   def post(self, request):
      if request.user.is_authenticated:
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save(supporter=request.user)
          return Response(
              serializer.data,
              status=status.HTTP_201_CREATED
          )
      return Response(
          serializer.errors,
          status=status.HTTP_400_BAD_REQUEST
          )
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
           raise Http404

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
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)

       return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST
       )
class CategoryListCreate(APIView):
    def post(self, request):
       serializer = CategorySerializer(data=request.data)
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
      categories = Category.objects.all()
      serializer = CategorySerializer(categories, many=True)
      return Response(serializer.data)