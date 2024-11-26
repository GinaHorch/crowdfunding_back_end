"""
URL configuration for crowdfunding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import CustomAuthToken as UserAuthToken
from organisations.views import CustomAuthToken as OrgAuthToken
from django.conf import settings
from django.conf.urls.static import static
from projects.views import CategoryListCreate
from django.http import JsonResponse
from django.urls import path, include


urlpatterns = [
    path('', lambda request: JsonResponse({"message": "Welcome to the API!"})),
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api-token-auth/users/', UserAuthToken.as_view(), name='api_token_auth_users'),
    path('api-token-auth/organisations/', OrgAuthToken.as_view(), name='api_token_auth_organisations'),
    path('organisations/', include('organisations.urls')),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
]
if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
