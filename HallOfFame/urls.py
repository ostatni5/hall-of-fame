"""HallOfFame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path

from hallOfFameClient.admin import lecturer_admin_site, default_admin_site

name = "root"
urlpatterns = [
    path('', include('hallOfFameWorld.urls')),
    # path('', include('hallOfFameClient.urls')),
    path('student/', include('hallOfFameStudent.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', default_admin_site.urls, name="admin"),
    path('lecturer/', lecturer_admin_site.urls, name="lecturer"),
    # path('lecturer/', include('hallOfFameClient.urls'))  # Felt cute, might delete later
]
