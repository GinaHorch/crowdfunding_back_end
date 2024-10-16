from django.urls import path
from . import views
from .api_views import OrganisationManagementViewSet
 
urlpatterns = [
  path('organisations/', views.OrganisationProfileList.as_view()),
  path('organisations/<int:pk>/', views.OrganisationProfileDetail.as_view()),
]