"""efarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.contrib import admin

schema_view = get_schema_view(
   openapi.Info(
      title="E-Farm API",
      default_version='v1',
      description="Ad Hoc Implementation of E-Farm Application",
      contact=openapi.Contact(email="attahattah37@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    # Other URL patterns for the project
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("admin/", admin.site.urls),
    # app-specific URLs
    #path('dairy/', include('dairy.urls', namespace='dairy')),
    #path('dairy_inventory/', include('dairy_inventory.urls')),
    path('poultry/', include('poultry.urls', namespace='poultry')),
    path('poultry_inventory/', include('poultry_inventory.urls', namespace='poultry_inventory')),
    path('users/', include('users.urls', namespace='users'))

]
