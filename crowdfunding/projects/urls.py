from django.urls import path
from . import views
from .views import CategoryListCreate, ProjectList, ProjectCreate, ProjectDetail, PledgeList, PledgeDetail
 
urlpatterns = [
  path('projects/', ProjectList.as_view(), name='project-list'),
  path('projects/create/', ProjectCreate.as_view(), name='project-create'),
  path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
  path('pledges/', PledgeList.as_view(), name='pledge-list'),
  path('pledges/<int:pk>/', PledgeDetail.as_view(), name='pledge-detail'),
  path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
]