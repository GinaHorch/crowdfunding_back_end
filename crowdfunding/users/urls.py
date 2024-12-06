from django.urls import path
from . import views
from .api_views import TokenAuthView
from .views import (
    CustomUserList, 
    CustomUserDetail,
    OrganisationList,
    OrganisationDetail,
    SignupView
)

urlpatterns = [
    path('', CustomUserList.as_view(), name='user-list'), # List and create users
    path('<int:pk>/', CustomUserDetail.as_view(), name='user-detail'), # Get, update, delete a user
    path('signup/', SignupView.as_view(), name='signup'),
    path('api/token-auth/', TokenAuthView.as_view(), name='token-auth'), # Unified token authentication
    path('organisations/', OrganisationList.as_view(), name='organisation-list'),
    path('organisations/<int:pk>/', OrganisationDetail.as_view(), name='organisation-detail'),
]