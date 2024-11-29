from django.urls import path
from . import views
from .views import TokenAuthView, CustomUserList, CustomUserDetail

urlpatterns = [
    path('', views.CustomUserList.as_view(), name='user-list'), # List and create users
    path('<int:pk>/', views.CustomUserDetail.as_view(), name='user-detail'), # Get, update, delete a user
    path('api/token-auth/', TokenAuthView.as_view(), name='token-auth') # Unified token authentication
]