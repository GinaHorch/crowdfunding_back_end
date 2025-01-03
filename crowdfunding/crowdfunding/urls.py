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
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from users.views import SignupView
from users.api_views import TokenAuthView

urlpatterns = [
    path('', lambda request: JsonResponse({"message": "Welcome to the API!"})),
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),
    path('signup/', SignupView.as_view(), name='signup'),
    path('api-token-auth/', TokenAuthView.as_view(), name='api-token-auth'),
    path('api/', include ('users.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)