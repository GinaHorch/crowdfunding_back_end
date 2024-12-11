from django.urls import path
from .views import CategoryListCreate, ProjectList, ProjectCreate, ProjectDetail, PledgeList, PledgeDetail, ProjectPledgeCreateView
from django.http import JsonResponse
 
def debug_view(request):
    return JsonResponse({"message": "Projects URLs are being resolved!"})

urlpatterns = [
  path('', ProjectList.as_view(), name='project-list'),
  path('create/', ProjectCreate.as_view(), name='project-create'),
  path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),

  path('pledges/', PledgeList.as_view(), name='pledge-list'),
  path('pledges/<int:pk>/', PledgeDetail.as_view(), name='pledge-detail'),
  path('projects/<int:project_id>/pledges/', ProjectPledgeCreateView.as_view(), name='project-pledges'),

  path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
  
  path('debug/', debug_view, name='debug'),
]