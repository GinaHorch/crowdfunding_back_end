from django.urls import path
from . import views
from .views import CustomAuthToken

urlpatterns = [
    path('', views.CustomUserList.as_view(), name='user-list'),
    path('<int:pk>/', views.CustomUserDetail.as_view(), name='user-detail'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_toke_auth_users')
]