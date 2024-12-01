from django.urls import path
from . import views
from .views import CategoryListCreate
 
urlpatterns = [
  path('', views.ProjectList.as_view(), name='project-list'),  # List and create projects
  path('<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
  path('pledges/', views.PledgeList.as_view(), name='pledge-list'),
  path('pledges/<int:pk>/', views.PledgeDetail.as_view(), name='pledge-detail'),
  path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
]