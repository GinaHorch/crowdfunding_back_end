from django.urls import path
from . import views
from .api_views import ProjectCreationViewSet
 
urlpatterns = [
  path('projects/', views.ProjectList.as_view()),
  path('projects/<int:pk>/', views.ProjectDetail.as_view()),
  path('pledges/', views.PledgeList.as_view()),
  path('pledges/<int:pk>/', views.PledgeDetail.as_view()),
]