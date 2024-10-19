from django.urls import path
from . import views
from .api_views import ProjectCreationViewSet
from .views import CategoryListCreate
from organisations.views import OrganisationProfileList, OrganisationProfileDetail
 
urlpatterns = [
  path('projects/', views.ProjectList.as_view()),
  path('projects/<int:pk>/', views.ProjectDetail.as_view()),
  path('pledges/', views.PledgeList.as_view()),
  path('pledges/<int:pk>/', views.PledgeDetail.as_view()),
  path('categories', CategoryListCreate.as_view(), name='category-list-create'),
  path('organisations/', OrganisationProfileList.as_view(), name='organisation-list-create'),
  path('organisations/<int:pk>/', OrganisationProfileDetail.as_view(), name='organisation-detail'),
]