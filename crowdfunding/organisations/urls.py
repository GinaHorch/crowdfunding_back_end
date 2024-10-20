from django.urls import path
from . import views
from .api_views import OrganisationManagementViewSet
from .views import OrganisationProfileList, OrganisationProfileDetail
 
urlpatterns = [
  path('', OrganisationProfileList.as_view(), name='organisation-list-create'),
  path('<int:pk>/', OrganisationProfileDetail.as_view(), name='organisation-detail'),
]